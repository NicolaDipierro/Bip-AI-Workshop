import logging
import os
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
    newOrder = order.model_dump()
    orders.append(newOrder)
    return {    
         "message": "Order created",
         "order": newOrder
}

