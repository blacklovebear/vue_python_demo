/**
 * Created by aresn on 16/6/20.
 */
import Vue from 'vue';
import VueRouter from 'vue-router';
import App from 'components/app.vue';

// use bootstrap
import 'bootstrap-webpack';


Vue.use(VueRouter);

// 开启debug模式
// Vue.config.debug = true;

// 路由配置
var router = new VueRouter({
    // 是否开启HTML5的history模式,开启后,需服务端支持,否则404
    history: false
});

router.map({
    '/': {
      name: 'index',
      component: require('./routers/conf_list.vue'),
    },
    '/detail/:conf_id/': {
      name: 'conf_detail',
      component: require('./routers/conf_detail.vue'),
    },
    '/jsonview/:conf_id': {
      name: 'jsonview',
      component: require('./routers/json_view.vue'),
    },
    '/conf/info': {
      name: 'confInfo',
      component: require('./routers/conf_info.vue'),
    },
    '/group/list': {
      name: 'groupList',
      component: require('./routers/group_list.vue'),
    },
    '/group/info': {
      name: 'groupInfo',
      component: require('./routers/group_info.vue'),
    },
});

router.beforeEach(() => {
    window.scrollTo(0, 0);
});

router.afterEach((transition) => {

});

router.redirect({
    '*': "/"
});

router.start(App, '#app');