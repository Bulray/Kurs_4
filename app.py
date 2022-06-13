from flask import Flask, render_template, request, redirect, url_for
from equipment import Equipment
from classes import unit_classes
from base import Arena
from unit import PlayerUnit, EnemyUnit, BaseUnit
import equipment

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes.get("player"), enemy=heroes.get("enemy"))
    return render_template("fight.html", heroes=heroes, result="Бой начался!")


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post'])
def choose_hero_to_post():
    name = request.form["name"]
    name_of_armor = request.form["armor"]
    name_of_weap = request.form["weapon"]
    unit_class = request.form["unit_class"]
    player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))
    player.equip_weapon(Equipment().get_weapon(name_of_weap))
    player.equip_armor(Equipment().get_armor(name_of_armor))
    heroes["player"] = player
    return redirect(url_for("/choose_enemy/"))


@app.route("/choose-hero/", methods=['get'])
def choose_hero_to_get():
    header = "Выберите героя"
    equipment = Equipment()
    weapons = equipment.get_weapons_names()
    armors = equipment.get_armors_names()
    classes = unit_classes
    return render_template(
        "hero_choosing.html",
        result={
            "header": header,
            "classes": classes,
            "weapons": weapons,
            "armors": armors
        }
    )


@app.route("/choose-enemy/", methods=['post'])
def choose_enemy_to_post():
    name = request.form["name"]
    name_of_armor = request.form["armor"]
    name_of_weap = request.form["weapon"]
    unit_class = request.form["unit_class"]
    enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))
    enemy.equip_weapon(Equipment().get_weapon(name_of_weap))
    enemy.equip_armor(Equipment().get_armor(name_of_armor))
    heroes["enemy"] = enemy
    return redirect(url_for("/start_fight/"))


@app.route("/choose-enemy/", methods=['get'])
def choose_enemy_to_get():
    header = "Выберите врага"
    equipment = Equipment()
    weapons = equipment.get_weapons_names()
    armors = equipment.get_armors_names()
    classes = unit_classes
    return render_template("hero_choosing.html",
        result={
            "header": header,
            "classes": classes,
            "weapons": weapons,
            "armors": armors
        }
    )


if __name__ == "__main__":
    app.run()
