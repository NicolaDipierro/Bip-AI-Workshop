targetScope = 'resourceGroup'

@description('Location')
param location string = resourceGroup().location

@description('Azure Container Registry Name')
param acrName string

@description('Name of the Log Analytics workspace backing the environment')
param logAnalyticsWorkspaceName string

@description('Container App Environment Name')
param containerEnvironmentName string

@description('Container App Name')
param containerAppName string

@description('Container Image')
param containerImage string

@description('Target port the container listens on')
param targetPort int = 80

@description('Minimum number of replicas')
param minReplicas int = 1

@description('Maximum number of replicas')
param maxReplicas int = 3

@description('CPU cores allocated to the container')
param cpuCores string = '0.5'

@description('Memory allocated to the container')
param memorySize string = '1Gi'

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location

  sku: {
    name: 'Basic'
  }

  properties: {
    adminUserEnabled: false
  }
}

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsWorkspaceName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource containerEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: containerEnvironmentName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

resource containerApp 'Microsoft.App/containerApps@2025-01-01' = {
  name: containerAppName
  location: location

  properties: {
    managedEnvironmentId: containerEnvironment.id

    configuration: {
      ingress: {
        external: true
        targetPort: targetPort
      }
    }

    template: {
      containers: [
        {
          name: 'api'
          image: containerImage

          resources: {
            cpu: json(cpuCores)
            memory: memorySize
          }
        }
      ]

      scale: {
        minReplicas: minReplicas
        maxReplicas: maxReplicas
      }
    }
  }
}

output containerAppFqdn string = containerApp.properties.configuration.ingress.fqdn
