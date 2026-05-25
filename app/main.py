from fastapi import FastAPI

from app.api.v1.routes import products, auth, cart, orders

app = FastAPI(title="Market API")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)