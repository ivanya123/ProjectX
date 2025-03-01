import flet as ft
from app.router import Router

def main(page: ft.Page):
    Router(page)


if __name__ == '__main__':
    ft.app(target=main)