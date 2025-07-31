from app import CurrencyApp

def test_convert_basic():
    app = CurrencyApp()
    result = app.convert("USD", "ARS", 100)
    assert result is not None
    assert "result" in result
    assert result["result"] > 0

def test_searchCod():
    app = CurrencyApp()
    assert app.searchCod("Euro") == "EUR"
    assert app.searchCod("Peso") == ""

### COMPLETAR PRUEBAS DE METODOS ###

