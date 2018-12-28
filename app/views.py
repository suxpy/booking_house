from datetime import datetime
import os
import re

from flask import Blueprint, request, render_template, \
    jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_, or_

from app.models import User, Area, Facility, House, HouseImage, Order
from utils import status_code
from utils.functions import is_login, check_id_card
from utils.settings import MEDIA_PATH
import random

user_blue = Blueprint('user', __name__)
order_blue = Blueprint('order', __name__)
house_blue = Blueprint('house', __name__)


@user_blue.route('/img_code/', methods=['GET'])
def img_code():
    seed = "1234567890"
    sa = []
    for i in range(4):
        sa.append(random.choice(seed))
    code = ''.join(sa)
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blue.route('/register/', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':

        return render_template('register.html')

    if request.method == 'POST':
        phone = request.form.get('phone')
        i_code = request.form.get('i_code')
        i_i_code = request.form.get('i_i_code')
        password = request.form.get('password')
        if i_code == i_i_code:
            user = User()
            user.phone = phone
            # from werkzeug.security import generate_password_hash
            password = generate_password_hash(password)
            user.pwd_hash = password

            user.save()
            return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blue.route('/login/', methods=['POST'])
def my_login():
    phone = request.form.get('phone')
    password = request.form.get('password')
    # 校验字段的完整性
    if not all([phone, password]):
        return jsonify(status_code.USER_LOGIN_PARAMS_IS_INVALID)
    # 判断用户是否注册
    user = User.query.filter(User.phone == phone).first()
    if not user:
        return jsonify({'code': 10002, 'msg': '用户没有注册，请去注册'})
    # 校验密码
    if not check_password_hash(user.pwd_hash, password):
        return jsonify({'code': 10003, 'msg': '密码不正确'})
    session['user_id'] = user.id
    return jsonify({'code': 200, 'msg': '请求成功'})


@house_blue.route('/index/', methods=['GET'])
def index():

    return render_template('index.html',)


@house_blue.route('/index_auth_user/', methods=['GET'])
def auth_user():
    choice = True
    if session['user_id']:
        choice = False
        user = User.query.get(session['user_id'])
        user_name = user.name
        return jsonify(code=200, choice=choice, user_name=user_name)
    return jsonify(code=200, choice=choice)


@user_blue.route('/center_info/', methods=['GET'])
def center_info():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    user_name = user.name
    user_phone = user.phone
    return jsonify({'code': 200, 'msg': '请求成功', 'user_name': user_name, 'user_phone': user_phone})


@user_blue.route('/my/', methods=['GET'])
def my():
    return render_template('my.html')


@user_blue.route('/change_info/', methods=['GET'])
def change_info():
    return render_template('profile.html')


@user_blue.route('/change_info/', methods=['PATCH'])
def my_change_info():
    user_id = session['user_id']
    avatar = request.files.get('avatar')
    if avatar:
        path = os.path.join(MEDIA_PATH, avatar.filename)
        avatar.save(path)
        user = User.query.filter(User.id == user_id).first()
        user.avatar = avatar.filename
        user.save()
        icon = avatar.filename
    return jsonify({'code': 200, 'msg': '请求成功', 'icon': icon})


@user_blue.route('/change_info_name/', methods=['POST'])
def my_change_info_name():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    user_name = request.form.get('user_name')
    user.name = str(user_name)
    user.save()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


@user_blue.route('/confirm/', methods=['GET'])
def confirm():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    real_name = user.id_name
    id_card = user.id_card
    return jsonify({'code': 200, 'msg': '请求成功', 'real_name': real_name, 'id_card': id_card})


@user_blue.route('/auth/', methods=['POST'])
def my_auth():
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    regex_name = r'[\u4E00-\u9FA5]{2,}'
    if not re.match(regex_name, real_name):
        return jsonify({'code': 500, 'msg': '姓名或身份证不符合格式'})
    if check_id_card(id_card):
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        user.id_name = real_name
        user.id_card = id_card
        user.save()
        return jsonify({'code': 200, 'msg': '请求成功'})
    else:
        return jsonify({'code': 500, 'msg': '姓名或身份证不符合格式'})


@user_blue.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


@user_blue.route('/show_myhouse/', methods=['GET'])
def show():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    id_name = user.id_name
    houses_list = House.query.filter(House.user_id == user_id)
    # area_json = [area.to_dict() for area in areas]
    houses_list_json = [house.to_dict() for house in houses_list]
    return jsonify({'code': 200, 'msg': '请求成功', 'houses_list': houses_list_json, 'id_name': id_name})


@user_blue.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@user_blue.route('/areas_facility/', methods=['POST'])
def areas_facility():
    areas = Area.query.all()
    facilitys = Facility.query.all()
    area_json = [area.to_dict() for area in areas]
    facility_json = [facility.to_dict() for facility in facilitys]
    return jsonify({'code': 200, 'msg': '请求成功', 'area_json': area_json, 'facility_json': facility_json})


@user_blue.route('/newhouse/', methods=['POST'])
def my_newhouse():
    house_dict = request.form
    house = House()
    house.user_id = session['user_id']
    house.price = house_dict.get('price')
    house.title = house_dict.get('title')
    house.area_id = house_dict.get('area_id')
    house.address = house_dict.get('address')
    house.room_count = house_dict.get('room_count')
    house.acreage = house_dict.get('acreage')
    house.unit = house_dict.get('unit')
    house.capacity = house_dict.get('capacity')
    house.beds = house_dict.get('beds')
    house.deposit = house_dict.get('deposit')
    house.min_days = house_dict.get('min_days')
    house.max_days = house_dict.get('max_days')
    facilities = house_dict.getlist('facility')
    f = []
    for facility_id in facilities:
        facility = Facility.query.get(facility_id)
        f.append(facility)
    house.facilities += f
    house.add_update()

    return jsonify(code=200, house_id=house.id)


@user_blue.route('/newhouse/', methods=['PATCH'])
def house_image():
    house_id = request.form.get('house_id')
    image = request.files.get('house_image')
    if image:
        path = os.path.join(MEDIA_PATH, image.filename)
        image.save(path)
        house_image = HouseImage()
        house_image.house_id = house_id
        house_image.url = image.filename
        house_image.add_update()
        images = []
        images.append(image.filename)
        house = House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url = images[0]
            house.add_update()
    return jsonify({'code': 200, 'msg': '请求成功', 'images': images})


@house_blue.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blue.route('/house_detail/<int:id>/', methods=['GET'])
def house_detail(id):
    make_order = True
    house = House.query.get(id)
    session['house_id'] =  house.id
    if session.get('user_id'):
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        user_houses = user.houses
        if house in user_houses:
            make_order = False

    house_json = [house.to_full_dict()]
    return jsonify(code=200, house=house_json, make_order=make_order)


@house_blue.route('/booking/', methods=['GET'])
@is_login
def booking():
    return render_template('booking.html')


@house_blue.route('/booking/', methods=['POST'])
def my_booking():
    house_id = session['house_id']
    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')

    house = House.query.get(house_id)

    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = request.form.get('days')
    order.house_price = request.form.get('price')
    order.amount = request.form.get('amount')

    order.add_update()

    return jsonify(code=200)


@user_blue.route('/my_orders/', methods=['GET'])
def orders():
    return render_template('orders.html')


@user_blue.route('/my_orders/', methods=['POST'])
def my_orders():
    return render_template('orders.html')


@user_blue.route('/lorders/', methods=['GET'])
@is_login
def get_myorders():
    user_id = session.get('user_id')
    orders = Order.query.filter(Order.user_id == user_id).order_by('-create_time').all()
    data = []
    for order in orders:
        order = order.to_dict()
        data.append(order)

    return jsonify({'code':200,'orders':data})

# 客户订单
def lorders():
    return render_template('lorders.html')


@user_blue.route('/show_lorders/', methods=['GET'])
def show_lorders():
    user_id = session['user_id']
    houses = House.query.filter(House.user_id == user_id)
    houses_ids = [house.id for house in houses]

    orders = Order.query.filter(Order.house_id.in_(houses_ids))
    if orders:
        orders_list = [order.to_dict() for order in orders]
        return jsonify(code=200, order_list=orders_list)


@house_blue.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


# @house_blue.route('/my_search/', methods=['GET'])
# def search_house():
#
#     aid = request.args.get('aid')
#     sd = request.args.get('sd')
#     ed = request.args.get('ed')
#     sk = request.args.get('sk')
#     # 过滤区域信息
#     house = House.query.filter(House.area_id==aid)
#     # 过滤登录用户发布房屋信息
#     if 'user_id' in session:
#         hlist = house.filter(House.user_id != session['user_id'])
#     # 查询不满足条件的房屋id
#     order1 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= ed)
#     order2 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= sd)
#     order3 = Order.query.filter(Order.begin_date >= sd, Order.begin_date <= ed)
#     order4 = Order.query.filter(Order.begin_date >= sd, Order.end_date <= ed)
#     house_ids1 = [order.house_id for order in order1]
#     house_ids2 = [order.house_id for order in order2]
#     house_ids3 = [order.house_id for order in order3]
#     house_ids4 = [order.house_id for order in order4]
#
#     house_ids = list(set(house_ids1 + house_ids2 + house_ids3 + house_ids4))
#     # 最终展示的房屋信息
#     houses = hlist.filter(House.id.notin_(house_ids))
#
#     if sk == 'booking':
#         houses = houses.order_by('order_count')
#     elif sk == 'price-inc':
#         houses = houses.order_by('price')
#     elif sk == 'price-des':
#         houses = houses.order_by('-price')
#     else:
#         houses = houses.order_by('-id')
#
#     houses_dict = [house.to_dict() for house in houses]
#
#     return jsonify(code=200, house=houses_dict)


@house_blue.route('/search/', methods = ['POST'])
def search_post():
    form = request.form
    aid = form.get('aid')
    sd = form.get('sd')
    ed = form.get('ed')
    # 根据地区筛选出house
    if aid:
        houses = House.query.filter(House.area_id == aid)
    else:
        houses = House.query.all()
    area_house_id = {house.id for house in houses}
    # 得到正在使用的house
    orders = Order.query.filter(Order.status.in_(["WAIT_ACCEPT", "WAIT_PAYMENT", "PAID"]))
    # 根据时间来筛选house
    if (sd and ed):
        sd = datetime.strptime(sd, "%Y-%m-%d")
        ed = datetime.strptime(ed, "%Y-%m-%d")
        house_inuse = orders.filter(or_(and_(Order.end_date <= ed, Order.end_date >= sd),and_(Order.begin_date <= ed, Order.begin_date >= sd)))
        hosue_inuse_id = set([house.house_id for house in house_inuse])
    else:
        # 如果开始时间，结束时间没填全，就不做筛选
        hosue_inuse_id = set()

    house_can_order_id = list(area_house_id-hosue_inuse_id)
    if not house_can_order_id:
        return jsonify({'code':1001,'msg':'没有房子'})

    # 封装数据
    data = []
    for id in house_can_order_id:
        house = houses.filter(House.id == id).first()
        msg = house.to_full_dict()
        # 入住人数
        num = len(house.orders)
        msg['num']=num
        # 创建时间
        create_time = house.create_time
        msg['create_time']=create_time
        data.append(msg)
    # 排序
    sort_key = form.get('sort_key')
    if sort_key == 'num':
        # 根据入住人数
        data = sorted(data,key = lambda msg:msg['num'],reverse = True)
    elif sort_key == 'price_asc':
        # 根据价格升序
        data = sorted(data,key = lambda msg:msg['price'])
    elif sort_key == 'price_desc':
        # 根据价格降序
        data = sorted(data,key = lambda msg:msg['price'],reverse = True)
    else:
        # 根据上线时间(默认)
        data = sorted(data, key = lambda msg: msg['create_time'], reverse = True)
    return jsonify({'code':200,'houses':data})
