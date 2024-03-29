from flask import render_template, Flask, request, url_for
from werkzeug.utils import redirect

from base import Arena
from equipment import Equipment
from classes import unit_classes
from unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": ...,
    "enemy": ...
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    if request.method == 'GET':
        header = 'Выбор героя'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'headers': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']
        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        if player.equip_armor(Equipment().get_armor(armor_name)) == None:
            raise ValueError('Нет такой брони.')
        if player.equip_weapon(Equipment().get_weapon(weapon_name)) == None:
            raise ValueError('Нет такого оружия.')

        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    if request.method == 'GET':
        header = 'Выбор противника'
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'headers': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        if enemy.equip_armor(Equipment().get_armor(armor_name)) == None:
            raise ValueError('Нет такой брони.')
        if enemy.equip_weapon(Equipment().get_weapon(weapon_name)) == None:
            raise ValueError('Нет такого оружия.')

        heroes['player'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
