"""
GameCafeteria Products Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import CafeteriaProduct, Game, User
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/cafeteria", status_code=status.HTTP_201_CREATED)
async def create_cafeteria_product(
    name: str,
    price: float,
    category: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new cafeteria product
    Only managers and admins
    """
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can create products"
        )
    
    product = CafeteriaProduct(
        name=name,
        price=price,
        category=category
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/cafeteria/")
async def list_cafeteria_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all cafeteria products
    """
    products = db.query(CafeteriaProduct).all()
    return products

@router.post("/games", status_code=status.HTTP_201_CREATED)
async def create_game(
    name: str,
    genre: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new game
    Only managers and admins
    """
    if current_user.role not in ["manager", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers and admins can create games"
        )
    
    game = Game(
        name=name,
        genre=genre
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

@router.get("/games/")
async def list_games(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all games
    """
    games = db.query(Game).all()
    return games
