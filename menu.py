from colorama import init, Fore, Back, Style

_W = 56  # ancho de columna de opciones


def menu(telegram=0):
    if telegram == 1:
        return (
            '0. Borrar todo\n'
            '1. Subir datos a SharePoint\n'
            '2. Descargar datos (ayer)\n'
            '3. Descargar datos (fecha específica)\n'
            '4. Descargar comentarios (fecha específica)\n'
            '5. Salir\n'
            f'{"─── DEV " + "─" * (_W - 8)}\n'
            '6. Descargar múltiples fechas (Turnero)\n'
            '7. Descargar rango de fechas (Turnero o Comentarios)'
        )

    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    init()

    # ── Header ───────────────────────────────────────────────────
    border = "═" * _W
    print()
    print(Fore.CYAN + Style.BRIGHT + f"╔{border}╗")
    print(f"║{'CIDI SCRAPPER  ─  EPEC':^{_W}}║")
    print(f"║{'Sistema de Atención Comercial':^{_W}}║")
    print(f"╚{border}╝" + Style.RESET_ALL)
    print()

    # ── Opciones principales ─────────────────────────────────────
    for opt in [
        "  0.  Borrar todo",
        "  1.  Subir datos a SharePoint",
        "  2.  Descargar datos (ayer)",
        "  3.  Descargar datos (fecha específica)",
        "  4.  Descargar comentarios (fecha específica)",
        "  5.  Salir",
    ]:
        print(Back.GREEN + Fore.WHITE + Style.BRIGHT + opt.ljust(_W) + Style.RESET_ALL)

    # ── Sección DEV ──────────────────────────────────────────────
    print()
    print(Fore.YELLOW + Style.BRIGHT + "─── DEV " + "─" * (_W - 8) + Style.RESET_ALL)

    for opt in [
        "  6.  Descargar múltiples fechas (Turnero)",
        "  7.  Descargar rango de fechas (Turnero o Comentarios)",
    ]:
        print(Back.YELLOW + Fore.BLACK + opt.ljust(_W) + Style.RESET_ALL)

    print()
