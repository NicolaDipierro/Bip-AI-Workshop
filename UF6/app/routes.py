import logging
import os
from fastapi import HTTPException
from fastapi import APIRouter

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
    # TODO
    pass


@router.get("/orders")
def get_orders():
    # TODO
    pass


@router.post("/orders")
def create_order(order):
    # TODO
    pass
