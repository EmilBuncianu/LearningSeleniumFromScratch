import logging
import pytest
from pytest_bdd import given, when, then

logger = logging.getLogger(__name__)

@given("I am a logged-in user on the inventory page")
def logged_in_user(driver):
    logger.info("--- [BDD START] Pornire scenariu: Finalizare achiziție ---")
    # ... restul codului tău ...

@then("the order should be finalized with a success message")
def verify_order_completion(driver):
    # ... logica ta de aserțiune ...
    logger.info("--- [BDD SUCCESS] Comanda a fost plasată cu succes! ---")
