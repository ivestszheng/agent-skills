#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import time
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "张三", "avatar": "https://tdesign.gtimg.com/site/avatar1.png"},
    {"id": 2, "name": "李四", "avatar": "https://tdesign.gtimg.com/site/avatar2.png"},
    {"id": 3, "name": "王五", "avatar": "https://tdesign.gtimg.com/site/avatar3.png"},
]

products = [
    {"id": 1, "title": "商品标题1", "desc": "这是商品1的描述内容", "price": "¥99.00", "sales": 1234, "image": "https://tdesign.gtimg.com/site/product1.png", "badge": "热销"},
    {"id": 2, "title": "商品标题2", "desc": "这是商品2的描述内容", "price": "¥199.00", "sales": 567, "image": "https://tdesign.gtimg.com/site/product2.png", "badge": "新品"},
    {"id": 3, "title": "商品标题3", "desc": "这是商品3的描述内容", "price": "¥299.00", "sales": 890, "image": "https://tdesign.gtimg.com/site/product3.png", "badge": ""},
    {"id": 4, "title": "商品标题4", "desc": "这是商品4的描述内容", "price": "¥399.00", "sales": 456, "image": "https://tdesign.gtimg.com/site/product4.png", "badge": "限时"},
]

reviews = [
    {"id": 1, "name": "用户A", "rate": 5, "content": "商品质量很好，非常满意！"},
    {"id": 2, "name": "用户B", "rate": 4, "content": "物流很快，包装完好，值得推荐。"},
    {"id": 3, "name": "用户C", "rate": 5, "content": "第二次购买了，一如既往的好。"},
]

specs = [
    {"name": "品牌", "value": "TDesign"},
    {"name": "型号", "value": "TD-001"},
    {"name": "颜色", "value": "白色"},
    {"name": "尺寸", "value": "M"},
    {"name": "材质", "value": "纯棉"},
]

@app.route('/api/products', methods=['GET'])
def get_products():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    keyword = request.args.get('keyword', '')
    
    filtered = products
    if keyword:
        filtered = [p for p in products if keyword.lower() in p['title'].lower()]
    
    start = (page - 1) * page_size
    end = start + page_size
    
    result = {
        "code": 0,
        "message": "success",
        "data": {
            "list": filtered[start:end],
            "total": len(filtered),
            "page": page,
            "page_size": page_size,
        }
    }
    
    time.sleep(0.5)
    return jsonify(result)

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product_detail(id):
    product = next((p for p in products if p['id'] == id), None)
    
    if not product:
        return jsonify({"code": 404, "message": "商品不存在"}), 404
    
    detail = {
        **product,
        "specs": specs,
        "reviews": reviews,
    }
    
    result = {
        "code": 0,
        "message": "success",
        "data": detail,
    }
    
    time.sleep(0.5)
    return jsonify(result)

@app.route('/api/users', methods=['GET'])
def get_users():
    result = {
        "code": 0,
        "message": "success",
        "data": users,
    }
    return jsonify(result)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        user = users[0]
        result = {
            "code": 0,
            "message": "登录成功",
            "data": {
                "user": user,
                "token": "mock-token-" + str(random.randint(1000, 9999)),
            },
        }
    else:
        result = {
            "code": 400,
            "message": "用户名或密码不能为空",
        }
    
    time.sleep(0.3)
    return jsonify(result)

@app.route('/api/form/submit', methods=['POST'])
def submit_form():
    data = request.get_json()
    
    result = {
        "code": 0,
        "message": "提交成功",
        "data": {
            "id": random.randint(1000, 9999),
            "created_at": datetime.now().isoformat(),
            "form_data": data,
        }
    }
    
    time.sleep(0.5)
    return jsonify(result)

@app.route('/api/banners', methods=['GET'])
def get_banners():
    banners = [
        {"id": 1, "image": "https://tdesign.gtimg.com/site/banner1.png", "link": "/pages/home"},
        {"id": 2, "image": "https://tdesign.gtimg.com/site/banner2.png", "link": "/pages/list"},
        {"id": 3, "image": "https://tdesign.gtimg.com/site/banner3.png", "link": "/pages/detail"},
    ]
    
    result = {
        "code": 0,
        "message": "success",
        "data": banners,
    }
    return jsonify(result)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"code": 404, "message": "接口不存在"}), 404

if __name__ == '__main__':
    print("=" * 50)
    print("TDesign Miniprogram Mock Server")
    print("=" * 50)
    print("运行地址: http://localhost:5000")
    print("可用接口:")
    print("  GET  /api/products          - 获取商品列表")
    print("  GET  /api/products/{id}     - 获取商品详情")
    print("  GET  /api/users             - 获取用户列表")
    print("  GET  /api/banners           - 获取轮播图")
    print("  POST /api/login             - 登录")
    print("  POST /api/form/submit       - 提交表单")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
