import logging
import os
import random
from time import time
from time import time
from venv import logger
from fastapi import HTTPException
from fastapi import APIRouter
from .models import Order

router = APIRouter()

API_KEY = "super-secret-api-key"

orders = []

@router.get("/")
def main():
    return {
        "message": "Hello, welcome to the Capstone Orders API!"
    }


@router.get("/health")
def health():
   return {
       "status": "UP"
}


@router.get("/orders")
def get_orders():
    return orders


@router.post("/orders")
def create_order(order: Order):
    order_correlation_id = os.urandom(16).hex()
    logger.info(f"Creating order: {order}, correlation_id: {order_correlation_id}")
    newOrder = order.model_dump()
    orders.append(newOrder)
    logger.info(f"Order created: {newOrder}, correlation_id: {order_correlation_id}")

    # call external service to process the order
    logger.info(f"Processing order: {newOrder}, correlation_id: {order_correlation_id}")
    return {    
         "message": "Order created",
         "order": newOrder
}


@router.post("/orders_error")
def create_order(order: Order):

    # Simulazione rallentamento
    time.sleep(random.randint(1, 5))

    # Simulazione errore casuale
    if random.randint(1, 10) > 7:

        raise Exception(
            "Database connection failed"
        )

    orders.append(
        order.model_dump()
    )

    return {
        "message": "Order created"
    }
