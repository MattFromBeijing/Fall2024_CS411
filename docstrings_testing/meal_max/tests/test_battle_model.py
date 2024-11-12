import pytest

from meal_max.models.battle_model import BattleModel
from meal_max.models.kitchen_model import Meal, update_meal_stats

@pytest.fixture
def battle_model():
    return BattleModel()

@pytest.fixture
def sample_meal1():
    return Meal(1, "Meal 1", "Chinese", 9.99, "HIGH")

@pytest.fixture
def sample_meal2():
    return Meal(2, "Meal 2", "American", 15.99, "LOW")

@pytest.fixture
def sample_meal3():
    return Meal(3, "Meal 3", "French", 19.99, "MED")

@pytest.fixture
def sample_meals(sample_meal1, sample_meal2):
    return [sample_meal1, sample_meal2]

##################################################
# Battle Test Case
##################################################

def test_battle(battle_model, sample_meal1, sample_meal2, mocker):
    """Test the battle between two meals"""

    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    # Mock get_random to return a fixed value
    mocker.patch('meal_max.models.battle_model.get_random', return_value=0.3)
    mock_update_meal_stats = mocker.patch('meal_max.models.battle_model.update_meal_stats')

    # Call battle
    winner_meal = battle_model.battle()

    assert winner_meal == sample_meal1.meal, f"Expected winner to be {sample_meal1.meal}, but got {winner_meal}"

    # Check that update_meal_stats was called correctly
    mock_update_meal_stats.assert_any_call(sample_meal1.id, 'win')
    mock_update_meal_stats.assert_any_call(sample_meal2.id, 'loss')

    # Ensure losing combatant was removed from combatants
    assert len(battle_model.combatants) == 1, "Expected only one combatant left after battle"
    assert battle_model.combatants[0] == sample_meal1, "Expected winner to remain in combatants"

def test_battle_low_combatants(battle_model, sample_meal1):
    """Testing a battle with less than 2 combatants"""
    battle_model.prep_combatant(sample_meal1)
    with pytest.raises(ValueError, match="Two combatants must be prepped for a battle."):
        battle_model.battle()

##################################################
# Remove Test Combatants Test Cases
##################################################

def test_clear_combatants(battle_model, sample_meal1):
    """Testing clearing combatants"""
    battle_model.prep_combatant(sample_meal1)

    battle_model.clear_combatants()

    assert len(battle_model.combatants) == 0, "Combatants should be empty after clearing"

##################################################
# Utility Function Test Cases
##################################################

def test_get_battle_score(battle_model, sample_meal1):
    """Testing retrieving the battle score of a meal"""
    battle_model.prep_combatant(sample_meal1)

    score = battle_model.get_battle_score(sample_meal1)

    assert score == 68.93, "Expected battle score of 68.93, but got {score}"

##################################################
# Meal Retrieval Test Cases
##################################################

def test_get_combatants(battle_model, sample_meal1):
    """Testing retrieving a meal"""
    battle_model.prep_combatant(sample_meal1)

    retrieved_list = battle_model.get_combatants()

    assert retrieved_list[0].id == 1
    assert retrieved_list[0].meal == 'Meal 1'
    assert retrieved_list[0].cuisine == 'Chinese'
    assert retrieved_list[0].price == 9.99
    assert retrieved_list[0].difficulty == 'HIGH'

##################################################
# Prep Meal Test Cases
##################################################

def test_prep_combatants(battle_model, sample_meal1):
    """Testing preparing a meal for battle"""
    battle_model.prep_combatant(sample_meal1)

    assert len(battle_model.combatants) == 1, "There should be one combatant in combatants"
    assert battle_model.combatants[0].meal == "Meal 1", "Meal 1 should have been added to combatants, but got {battle_model.combatants[0].meal} instead"

def test_prep_combatants_overload(battle_model, sample_meal1, sample_meal2, sample_meal3):
    """Testing preparing more than 2 meals for battle"""
    battle_model.prep_combatant(sample_meal1)
    battle_model.prep_combatant(sample_meal2)

    with pytest.raises(ValueError, match="Combatant list is full, cannot add more combatants."):
        battle_model.prep_combatant(sample_meal3)