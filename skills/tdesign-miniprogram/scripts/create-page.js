const fs = require('fs');
const path = require('path');

const targetType = process.argv[2];
const customPath = process.argv[3];

const pageTypes = ['home', 'list', 'form', 'detail'];

if (!targetType || !pageTypes.includes(targetType)) {
  console.error('用法: node create-page.js <页面类型> [自定义路径]');
  console.error('页面类型: home | list | form | detail');
  console.error('示例:');
  console.error('  node create-page.js home');
  console.error('  node create-page.js list pages/product/list');
  process.exit(1);
}

const pagePath = customPath || `pages/${targetType}/${targetType}`;
const dir = path.dirname(pagePath);
if (!fs.existsSync(dir)) {
  fs.mkdirSync(dir, { recursive: true });
}

const templates = {
  home: {
    wxml: `<view class="home-page">
  <t-navbar title="首页" />
  
  <view class="banner-section">
    <swiper class="banner" indicator-dots autoplay circular interval="3000">
      <swiper-item wx:for="{{banners}}" wx:key="id">
        <image src="{{item.image}}" mode="aspectFill" class="banner-img" />
      </swiper-item>
    </swiper>
  </view>

  <view class="grid-section">
    <t-grid column="4">
      <t-grid-item wx:for="{{gridItems}}" wx:key="id" icon="{{item.icon}}" label="{{item.label}}" bind:click="onGridClick" />
    </t-grid>
  </view>

  <view class="section">
    <view class="section-header">
      <text class="section-title">推荐内容</text>
      <text class="section-more">查看更多</text>
    </view>
    <view class="card-list">
      <view class="card" wx:for="{{cards}}" wx:key="id">
        <image src="{{item.image}}" mode="aspectFill" class="card-img" />
        <view class="card-content">
          <text class="card-title">{{item.title}}</text>
          <text class="card-desc">{{item.desc}}</text>
          <view class="card-footer">
            <t-badge content="{{item.badge}}" />
          </view>
        </view>
      </view>
    </view>
  </view>
</view>`,
    wxss: `.home-page {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.banner-section {
  margin-bottom: 20rpx;
}

.banner {
  height: 360rpx;
}

.banner-img {
  width: 100%;
  height: 100%;
  border-radius: 16rpx;
}

.grid-section {
  padding: 0 24rpx;
  margin-bottom: 20rpx;
  background-color: #fff;
}

.section {
  padding: 24rpx;
  margin-bottom: 20rpx;
  background-color: #fff;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: 600;
  color: #333;
}

.section-more {
  font-size: 26rpx;
  color: #999;
}

.card-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.card {
  width: calc(50% - 10rpx);
  border-radius: 16rpx;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.08);
}

.card-img {
  width: 100%;
  height: 240rpx;
}

.card-content {
  padding: 16rpx;
}

.card-title {
  font-size: 28rpx;
  font-weight: 500;
  color: #333;
  margin-bottom: 8rpx;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-desc {
  font-size: 24rpx;
  color: #999;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-footer {
  margin-top: 12rpx;
}`,
    js: `Page({
  data: {
    banners: [
      { id: 1, image: 'https://tdesign.gtimg.com/site/banner1.png' },
      { id: 2, image: 'https://tdesign.gtimg.com/site/banner2.png' },
      { id: 3, image: 'https://tdesign.gtimg.com/site/banner3.png' },
    ],
    gridItems: [
      { id: 1, icon: 'home', label: '首页' },
      { id: 2, icon: 'list', label: '列表' },
      { id: 3, icon: 'settings', label: '设置' },
      { id: 4, icon: 'user', label: '我的' },
      { id: 5, icon: 'search', label: '搜索' },
      { id: 6, icon: 'message', label: '消息' },
      { id: 7, icon: 'cart', label: '购物车' },
      { id: 8, icon: 'share', label: '分享' },
    ],
    cards: [
      { id: 1, image: 'https://tdesign.gtimg.com/site/card1.png', title: '商品标题1', desc: '商品描述内容', badge: '热销' },
      { id: 2, image: 'https://tdesign.gtimg.com/site/card2.png', title: '商品标题2', desc: '商品描述内容', badge: '新品' },
      { id: 3, image: 'https://tdesign.gtimg.com/site/card3.png', title: '商品标题3', desc: '商品描述内容', badge: '' },
      { id: 4, image: 'https://tdesign.gtimg.com/site/card4.png', title: '商品标题4', desc: '商品描述内容', badge: '限时' },
    ],
  },

  onLoad() {},

  onGridClick(e) {
    const { label } = e.currentTarget.dataset;
    wx.showToast({ title: \`点击了 ${label}\`, icon: 'none' });
  },
});`,
    json: `{
  "usingComponents": {
    "t-navbar": "tdesign-miniprogram/navbar/navbar",
    "t-grid": "tdesign-miniprogram/grid/grid",
    "t-grid-item": "tdesign-miniprogram/grid-item/grid-item",
    "t-badge": "tdesign-miniprogram/badge/badge"
  }
}`,
  },
  list: {
    wxml: `<view class="list-page">
  <t-navbar title="列表页" />
  
  <view class="search-section">
    <t-search placeholder="请输入搜索内容" value="{{searchValue}}" bind:change="onSearchChange" />
  </view>

  <view class="filter-section">
    <scroll-view scroll-x class="filter-scroll">
      <view class="filter-list">
        <view 
          wx:for="{{filters}}" 
          wx:key="id" 
          class="filter-item {{currentFilter === item.id ? 'active' : ''}}"
          bind:click="onFilterClick"
        >
          {{item.label}}
        </view>
      </view>
    </scroll-view>
  </view>

  <view class="list-content">
    <t-cell-group>
      <t-cell 
        wx:for="{{listData}}" 
        wx:key="id" 
        title="{{item.title}}" 
        sub-title="{{item.subTitle}}"
        hover
        bind:click="onItemClick"
      >
        <image slot="left-icon" src="{{item.icon}}" class="cell-icon" />
        <t-badge slot="extra" content="{{item.badge}}" wx:if="{{item.badge}}" />
        <text slot="extra" class="cell-extra">{{item.extra}}</text>
      </t-cell>
    </t-cell-group>
  </view>

  <t-loading wx:if="{{loading}}" />
</view>`,
    wxss: `.list-page {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.search-section {
  padding: 20rpx 24rpx;
  background-color: #fff;
}

.filter-section {
  background-color: #fff;
  margin-bottom: 20rpx;
}

.filter-scroll {
  white-space: nowrap;
}

.filter-list {
  display: inline-flex;
  padding: 20rpx 24rpx;
  gap: 32rpx;
}

.filter-item {
  padding: 12rpx 24rpx;
  font-size: 28rpx;
  color: #666;
  background-color: #f5f5f5;
  border-radius: 32rpx;
}

.filter-item.active {
  color: #fff;
  background-color: #1677ff;
}

.list-content {
  padding: 0 24rpx;
}

.cell-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 16rpx;
}

.cell-extra {
  font-size: 26rpx;
  color: #999;
}`,
    js: `Page({
  data: {
    searchValue: '',
    currentFilter: 'all',
    filters: [
      { id: 'all', label: '全部' },
      { id: 'hot', label: '热门' },
      { id: 'new', label: '最新' },
      { id: 'price', label: '价格' },
      { id: 'sales', label: '销量' },
    ],
    listData: [],
    loading: true,
    page: 1,
    pageSize: 10,
  },

  onLoad() {
    this.loadData();
  },

  onReachBottom() {
    if (!this.data.loading) {
      this.setData({ page: this.data.page + 1 });
      this.loadData();
    }
  },

  loadData() {
    this.setData({ loading: true });
    
    setTimeout(() => {
      const newData = Array.from({ length: this.data.pageSize }, (_, i) => ({
        id: (this.data.page - 1) * this.data.pageSize + i + 1,
        title: \`列表项 \${(this.data.page - 1) * this.data.pageSize + i + 1}\`,
        subTitle: '这是列表项的副标题描述内容',
        icon: 'https://tdesign.gtimg.com/site/icon.png',
        badge: Math.random() > 0.7 ? 'NEW' : '',
        extra: '查看',
      }));
      
      this.setData({
        listData: this.data.page === 1 ? newData : [...this.data.listData, ...newData],
        loading: false,
      });
    }, 800);
  },

  onSearchChange(e) {
    this.setData({ searchValue: e.detail.value });
  },

  onFilterClick(e) {
    const id = e.currentTarget.dataset.id;
    this.setData({ currentFilter: id, page: 1, listData: [] });
    this.loadData();
  },

  onItemClick(e) {
    const { title } = e.currentTarget.dataset;
    wx.showToast({ title: \`点击了 \${title}\`, icon: 'none' });
  },
});`,
    json: `{
  "usingComponents": {
    "t-navbar": "tdesign-miniprogram/navbar/navbar",
    "t-search": "tdesign-miniprogram/search/search",
    "t-cell": "tdesign-miniprogram/cell/cell",
    "t-cell-group": "tdesign-miniprogram/cell-group/cell-group",
    "t-badge": "tdesign-miniprogram/badge/badge",
    "t-loading": "tdesign-miniprogram/loading/loading"
  }
}`,
  },
  form: {
    wxml: `<view class="form-page">
  <t-navbar title="表单页" />
  
  <view class="form-content">
    <t-form label-width="120rpx">
      <t-cell-group>
        <t-cell title="姓名" required>
          <t-input slot="detail" placeholder="请输入姓名" value="{{formData.name}}" bind:change="onFormChange" data-field="name" />
        </t-cell>
        
        <t-cell title="手机号" required>
          <t-input slot="detail" type="number" placeholder="请输入手机号" value="{{formData.phone}}" bind:change="onFormChange" data-field="phone" />
        </t-cell>
        
        <t-cell title="邮箱">
          <t-input slot="detail" type="email" placeholder="请输入邮箱" value="{{formData.email}}" bind:change="onFormChange" data-field="email" />
        </t-cell>
        
        <t-cell title="性别">
          <view class="gender-group">
            <t-radio-group value="{{formData.gender}}" bind:change="onGenderChange">
              <t-radio value="male">男</t-radio>
              <t-radio value="female">女</t-radio>
            </t-radio-group>
          </view>
        </t-cell>
        
        <t-cell title="兴趣爱好">
          <view class="hobby-group">
            <t-checkbox-group value="{{formData.hobbies}}" bind:change="onHobbyChange">
              <t-checkbox value="reading">阅读</t-checkbox>
              <t-checkbox value="sports">运动</t-checkbox>
              <t-checkbox value="music">音乐</t-checkbox>
              <t-checkbox value="travel">旅行</t-checkbox>
            </t-checkbox-group>
          </view>
        </t-cell>
        
        <t-cell title="日期选择">
          <t-datetime-picker slot="detail" value="{{formData.date}}" type="date" bind:change="onDateChange" />
        </t-cell>
        
        <t-cell title="开关">
          <t-switch slot="detail" checked="{{formData.switch}}" bind:change="onSwitchChange" />
        </t-cell>
        
        <t-cell title="备注">
          <t-textarea slot="detail" placeholder="请输入备注信息" value="{{formData.remark}}" bind:change="onFormChange" data-field="remark" />
        </t-cell>
      </t-cell-group>
    </t-form>
  </view>

  <view class="form-footer">
    <t-button theme="default" size="large" style="width: 300rpx; margin-right: 20rpx;" bind:click="onReset">重置</t-button>
    <t-button theme="primary" size="large" style="width: 300rpx;" bind:click="onSubmit">提交</t-button>
  </view>
</view>`,
    wxss: `.form-page {
  background-color: #f5f5f5;
  min-height: 100vh;
}

.form-content {
  padding: 24rpx;
}

.gender-group {
  display: flex;
  gap: 40rpx;
}

.hobby-group {
  display: flex;
  flex-wrap: wrap;
  gap: 30rpx;
}

.form-footer {
  display: flex;
  padding: 24rpx;
  background-color: #fff;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
}`,
    js: `Page({
  data: {
    formData: {
      name: '',
      phone: '',
      email: '',
      gender: '',
      hobbies: [],
      date: '',
      switch: false,
      remark: '',
    },
  },

  onLoad() {},

  onFormChange(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({
      \`formData.\${field}\`: e.detail.value,
    });
  },

  onGenderChange(e) {
    this.setData({
      \`formData.gender\`: e.detail.value,
    });
  },

  onHobbyChange(e) {
    this.setData({
      \`formData.hobbies\`: e.detail.value,
    });
  },

  onDateChange(e) {
    this.setData({
      \`formData.date\`: e.detail.value,
    });
  },

  onSwitchChange(e) {
    this.setData({
      \`formData.switch\`: e.detail.checked,
    });
  },

  onSubmit() {
    const { formData } = this.data;
    
    if (!formData.name) {
      wx.showToast({ title: '请输入姓名', icon: 'none' });
      return;
    }
    
    if (!formData.phone) {
      wx.showToast({ title: '请输入手机号', icon: 'none' });
      return;
    }

    console.log('表单数据:', formData);
    
    wx.showToast({ title: '提交成功', icon: 'success' });
  },

  onReset() {
    this.setData({
      formData: {
        name: '',
        phone: '',
        email: '',
        gender: '',
        hobbies: [],
        date: '',
        switch: false,
        remark: '',
      },
    });
  },
});`,
    json: `{
  "usingComponents": {
    "t-navbar": "tdesign-miniprogram/navbar/navbar",
    "t-form": "tdesign-miniprogram/form/form",
    "t-cell": "tdesign-miniprogram/cell/cell",
    "t-cell-group": "tdesign-miniprogram/cell-group/cell-group",
    "t-input": "tdesign-miniprogram/input/input",
    "t-textarea": "tdesign-miniprogram/textarea/textarea",
    "t-radio": "tdesign-miniprogram/radio/radio",
    "t-radio-group": "tdesign-miniprogram/radio-group/radio-group",
    "t-checkbox": "tdesign-miniprogram/checkbox/checkbox",
    "t-checkbox-group": "tdesign-miniprogram/checkbox-group/checkbox-group",
    "t-datetime-picker": "tdesign-miniprogram/datetime-picker/datetime-picker",
    "t-switch": "tdesign-miniprogram/switch/switch",
    "t-button": "tdesign-miniprogram/button/button"
  }
}`,
  },
  detail: {
    wxml: `<scroll-view scroll-y class="detail-page">
  <t-navbar title="详情页" />
  
  <view class="detail-header">
    <image src="{{detail.image}}" mode="aspectFill" class="detail-img" />
    <view class="detail-info">
      <text class="detail-title">{{detail.title}}</text>
      <t-badge content="{{detail.badge}}" class="detail-badge" />
      <text class="detail-price">{{detail.price}}</text>
      <text class="detail-sales">销量 {{detail.sales}}</text>
    </view>
  </view>

  <view class="detail-section">
    <view class="section-header">
      <text class="section-title">商品详情</text>
    </view>
    <view class="section-content">
      <text class="detail-desc">{{detail.desc}}</text>
    </view>
  </view>

  <view class="detail-section">
    <view class="section-header">
      <text class="section-title">规格参数</text>
    </view>
    <t-cell-group>
      <t-cell wx:for="{{detail.specs}}" wx:key="name" title="{{item.name}}" value="{{item.value}}" />
    </t-cell-group>
  </view>

  <view class="detail-section">
    <view class="section-header">
      <text class="section-title">用户评价</text>
      <text class="section-count">{{detail.reviews.length}}条</text>
    </view>
    <view class="review-list">
      <view class="review-item" wx:for="{{detail.reviews}}" wx:key="id">
        <t-avatar icon="user" class="review-avatar" />
        <view class="review-content">
          <view class="review-header">
            <text class="review-name">{{item.name}}</text>
            <t-rate value="{{item.rate}}" disabled size="small" />
          </view>
          <text class="review-text">{{item.content}}</text>
        </view>
      </view>
    </view>
  </view>
</scroll-view>

<view class="detail-footer">
  <view class="footer-left">
    <view class="footer-btn">
      <text class="footer-icon">收藏</text>
      <text class="footer-text">收藏</text>
    </view>
    <view class="footer-btn">
      <text class="footer-icon">购物车</text>
      <text class="footer-text">购物车</text>
    </view>
  </view>
  <t-button theme="default" size="large" style="width: 200rpx;">加入购物车</t-button>
  <t-button theme="primary" size="large" style="width: 300rpx;">立即购买</t-button>
</view>`,
    wxss: `.detail-page {
  background-color: #f5f5f5;
  height: 100vh;
}

.detail-header {
  background-color: #fff;
  padding-bottom: 24rpx;
}

.detail-img {
  width: 100%;
  height: 600rpx;
}

.detail-info {
  padding: 24rpx;
}

.detail-title {
  font-size: 34rpx;
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 16rpx;
}

.detail-badge {
  margin-bottom: 16rpx;
}

.detail-price {
  font-size: 40rpx;
  font-weight: 600;
  color: #ff4d4f;
  display: block;
  margin-bottom: 8rpx;
}

.detail-sales {
  font-size: 26rpx;
  color: #999;
}

.detail-section {
  background-color: #fff;
  margin-top: 20rpx;
  padding: 24rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #333;
}

.section-count {
  font-size: 26rpx;
  color: #999;
}

.detail-desc {
  font-size: 28rpx;
  color: #666;
  line-height: 1.8;
}

.review-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.review-item {
  display: flex;
  gap: 16rpx;
}

.review-avatar {
  width: 80rpx;
  height: 80rpx;
}

.review-content {
  flex: 1;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12rpx;
}

.review-name {
  font-size: 28rpx;
  font-weight: 500;
  color: #333;
}

.review-text {
  font-size: 26rpx;
  color: #666;
  line-height: 1.6;
}

.detail-footer {
  display: flex;
  align-items: center;
  padding: 16rpx 24rpx;
  background-color: #fff;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  box-shadow: 0 -2rpx 12rpx rgba(0, 0, 0, 0.08);
}

.footer-left {
  display: flex;
  gap: 32rpx;
}

.footer-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.footer-icon {
  font-size: 40rpx;
}

.footer-text {
  font-size: 22rpx;
  color: #666;
  margin-top: 4rpx;
}`,
    js: `Page({
  data: {
    detail: {
      image: 'https://tdesign.gtimg.com/site/product.png',
      title: '商品标题名称，这是一个很长的商品标题',
      badge: '热销',
      price: '¥199.00',
      sales: '2341',
      desc: '这是商品的详细描述内容。商品采用优质材料制作，做工精细，品质保证。支持七天无理由退换货，让您购物无忧。',
      specs: [
        { name: '品牌', value: 'TDesign' },
        { name: '型号', value: 'TD-001' },
        { name: '颜色', value: '白色' },
        { name: '尺寸', value: 'M' },
        { name: '材质', value: '纯棉' },
      ],
      reviews: [
        { id: 1, name: '用户A', rate: 5, content: '商品质量很好，非常满意！' },
        { id: 2, name: '用户B', rate: 4, content: '物流很快，包装完好，值得推荐。' },
        { id: 3, name: '用户C', rate: 5, content: '第二次购买了，一如既往的好。' },
      ],
    },
  },

  onLoad(options) {
    if (options.id) {
      this.loadDetail(options.id);
    }
  },

  loadDetail(id) {
    console.log('加载商品详情:', id);
  },
});`,
    json: `{
  "usingComponents": {
    "t-navbar": "tdesign-miniprogram/navbar/navbar",
    "t-badge": "tdesign-miniprogram/badge/badge",
    "t-cell": "tdesign-miniprogram/cell/cell",
    "t-cell-group": "tdesign-miniprogram/cell-group/cell-group",
    "t-avatar": "tdesign-miniprogram/avatar/avatar",
    "t-rate": "tdesign-miniprogram/rate/rate",
    "t-button": "tdesign-miniprogram/button/button"
  }
}`,
  },
};

const { wxml, wxss, js, json } = templates[targetType];

const files = {
  [pagePath + '.wxml']: wxml,
  [pagePath + '.wxss']: wxss,
  [pagePath + '.js']: js,
  [pagePath + '.json']: json,
};

for (const [filePath, content] of Object.entries(files)) {
  fs.writeFileSync(filePath, content, 'utf-8');
  console.log(`已创建: ${filePath}`);
}

console.log('\n页面模板生成完成！');
console.log('请记得在 app.json 中注册新页面路径');
