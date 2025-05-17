<template>
    <div class="login-container flex z-10">
        <!-- 新增标题 -->
        <div class="login-title">
            基于网络爬虫的京东用户评论分析及可视化设计
        </div>

        <div class="login-right flex z-10">
            <div class="login-right-warp flex-margin">
                <span class="login-right-warp-one"></span>
                <span class="login-right-warp-two"></span>
                <div class="login-right-warp-mian">
                    <div class="login-right-warp-main-title"> 欢迎您！</div>
                    <div class="login-right-warp-main-form">
                        <div v-if="!state.isScan">
                            <el-tabs v-model="state.tabsActiveName">
                                <el-tab-pane :label="$t('message.label.one1')" name="account">
                                    <Account />
                                </el-tab-pane>
                            </el-tabs>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="login-authorization z-10">
        </div>
    </div>
    <div v-if="siteBg">
        <img :src="siteBg" class="fixed inset-0 z-1 w-full h-full" />
    </div>
</template>

<script setup lang="ts" name="loginIndex">
    import { defineAsyncComponent, onMounted, reactive, computed } from 'vue';
    import { storeToRefs } from 'pinia';
    import { useThemeConfig } from '/@/stores/themeConfig';
    import { NextLoading } from '/@/utils/loading';
    import logoMini from '/@/assets/logo-mini.svg';
    import { SystemConfigStore } from '/@/stores/systemConfig'
    import { getBaseURL } from "/@/utils/baseUrl";
    // 引入组件
    const Account = defineAsyncComponent(() => import('/@/views/system/login/component/account.vue'));
    const Mobile = defineAsyncComponent(() => import('/@/views/system/login/component/mobile.vue'));
    // const Scan = defineAsyncComponent(() => import('/@/views/system/login/component/scan.vue'));
    import _ from "lodash-es";

    // 定义变量内容
    const storesThemeConfig = useThemeConfig();
    const { themeConfig } = storeToRefs(storesThemeConfig);
    const state = reactive({
        tabsActiveName: 'account',
        isScan: false,
    });

    // 获取布局配置信息
    const getThemeConfig = computed(() => {
        return themeConfig.value;
    });

    const systemConfigStore = SystemConfigStore()
    const { systemConfig } = storeToRefs(systemConfigStore)
    const getSystemConfig = computed(() => {
        return systemConfig.value
    })

    const siteLogo = computed(() => {
        if (!_.isEmpty(getSystemConfig.value['login.site_logo'])) {
            return getSystemConfig.value['login.site_logo']
        }
        return logoMini
    });

    const siteBg = computed(() => {
        if (!_.isEmpty(getSystemConfig.value['login.login_background'])) {
            return getSystemConfig.value['login.login_background']
        }
    });

    // 页面加载时
    onMounted(() => {
        NextLoading.done();
    });
</script>

<style scoped lang="scss">
.login-container {
    height: 100vh; /* 使用视口高度确保全屏 */
    background: var(--el-color-white);
    background-image: url('/@/assets/image.png'); /* 替换为新的背景图片路径 */
    background-size: cover; /* 使背景图片覆盖整个容器 */
    background-position: center; /* 将背景图片居中 */
    background-repeat: no-repeat; /* 防止背景图片重复 */
    display: flex;
    flex-direction: column; /* 改为垂直布局 */
    align-items: flex-end; /* 将内容靠右对齐 */
    position: relative; /* 确保背景图片在容器内 */
    padding-right: 100px; /* 右侧留出一些空白 */

    /* 新增标题样式 */
    .login-title {
        position: absolute;
        top: 50px; /* 距离顶部50px */
        left: 50%; /* 水平居中 */
        transform: translateX(-50%); /* 水平居中 */
        font-size: 24px;
        font-weight: bold;
        color: var(--el-text-color-primary);
        text-align: center;
        z-index: 2; /* 确保标题在背景图片之上 */
    }

    .login-right {
        width: 500px;
        background-color: rgba(255, 255, 255, 0.8); /* 添加透明度以便背景图片可见 */
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        z-index: 2; /* 确保登录框在背景图片之上 */
        margin-top: 150px; /* 与标题保持一定距离 */

        .login-right-warp {
            border: 1px solid var(--el-color-primary-light-3);
            border-radius: 10px;
            width: 100%;
            height: 500px;
            position: relative;
            overflow: hidden;
            background-color: var(--el-color-white);

            .login-right-warp-one,
            .login-right-warp-two {
                position: absolute;
                display: block;
                width: inherit;
                height: inherit;

                &::before,
                &::after {
                    content: '';
                    position: absolute;
                    z-index: 1;
                }
            }

            .login-right-warp-one {
                &::before {
                    filter: hue-rotate(0deg);
                    top: 0px;
                    left: 0;
                    width: 100%;
                    height: 3px;
                    background: linear-gradient(90deg, transparent, var(--el-color-primary));
                    animation: loginLeft 3s linear infinite;
                }

                &::after {
                    filter: hue-rotate(60deg);
                    top: -100%;
                    right: 2px;
                    width: 3px;
                    height: 100%;
                    background: linear-gradient(180deg, transparent, var(--el-color-primary));
                    animation: loginTop 3s linear infinite;
                    animation-delay: 0.7s;
                }
            }

            .login-right-warp-two {
                &::before {
                    filter: hue-rotate(120deg);
                    bottom: 2px;
                    right: -100%;
                    width: 100%;
                    height: 3px;
                    background: linear-gradient(270deg, transparent, var(--el-color-primary));
                    animation: loginRight 3s linear infinite;
                    animation-delay: 1.4s;
                }

                &::after {
                    filter: hue-rotate(300deg);
                    bottom: -100%;
                    left: 0px;
                    width: 3px;
                    height: 100%;
                    background: linear-gradient(360deg, transparent, var(--el-color-primary));
                    animation: loginBottom 3s linear infinite;
                    animation-delay: 2.1s;
                }
            }

            .login-right-warp-mian {
                display: flex;
                flex-direction: column;
                height: 100%;

                .login-right-warp-main-title {
                    height: 130px;
                    line-height: 130px;
                    font-size: 27px;
                    text-align: center;
                    letter-spacing: 3px;
                    animation: logoAnimation 0.3s ease;
                    animation-delay: 0.3s;
                    color: var(--el-text-color-primary);
                }

                .login-right-warp-main-form {
                    flex: 1;
                    padding: 0 50px 50px;

                    .login-content-main-sacn {
                        position: absolute;
                        top: 2px;
                        right: 12px;
                        width: 50px;
                        height: 50px;
                        overflow: hidden;
                        cursor: pointer;
                        transition: all ease 0.3s;
                        color: var(--el-color-primary);

                        &-delta {
                            position: absolute;
                            width: 35px;
                            height: 70px;
                            z-index: 2;
                            top: 2px;
                            right: 21px;
                            background: var(--el-color-white);
                            transform: rotate(-45deg);
                        }

                        &:hover {
                            opacity: 1;
                            transition: all ease 0.3s;
                            color: var(--el-color-primary) !important;
                        }

                        i {
                            width: 47px;
                            height: 50px;
                            display: inline-block;
                            font-size: 48px;
                            position: absolute;
                            right: 1px;
                            top: 0px;
                        }
                    }
                }
            }
        }
    }

    .login-authorization {
        position: fixed;
        bottom: 30px;
        left: 0;
        right: 0;
        text-align: center;
        z-index: 2; /* 确保授权信息在背景图片之上 */

        p {
            font-size: 14px;
            color: rgba(0, 0, 0, 0.5);
        }

        a {
            color: var(--el-color-primary);
            margin: 0 5px;
        }
    }
}
</style>