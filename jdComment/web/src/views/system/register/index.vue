<template>
  <div class="register-container flex z-10">
    <!-- 新增标题 -->
    <div class="register-title">
      基于网络爬虫的京东用户评论分析及可视化设计
    </div>

    <div class="register-right flex z-10">
      <div class="register-right-warp flex-margin">
        <div class="register-right-warp-main">
          <div class="register-right-warp-main-title"> 注册新账号 </div>
          <div class="register-right-warp-main-form">
            <el-form ref="formRef" size="large" class="register-content-form" :model="state.ruleForm" :rules="rules" @keyup.enter="registerClick">
              <!-- 用户名 -->
              <el-form-item class="register-animation1" prop="username">
                <el-input type="text" :placeholder="'请输入用户名'" v-model="state.ruleForm.username" clearable autocomplete="off"></el-input>
              </el-form-item>

              <!-- 密码 -->
              <el-form-item class="register-animation2" prop="password">
                <el-input type="password" :placeholder="'请输入密码'" v-model="state.ruleForm.password" clearable autocomplete="off"></el-input>
              </el-form-item>

              <!-- 邮箱 -->
              <el-form-item class="register-animation3" prop="email">
                <el-input type="email" :placeholder="'请输入邮箱'" v-model="state.ruleForm.email" clearable autocomplete="off"></el-input>
              </el-form-item>

              <!-- 手机号 -->
              <el-form-item class="register-animation4" prop="mobile">
                <el-input type="tel" :placeholder="'请输入手机号'" v-model="state.ruleForm.mobile" clearable autocomplete="off"></el-input>
              </el-form-item>

              <!-- 姓名 -->
              <el-form-item class="register-animation6" prop="name">
                <el-input type="text" :placeholder="'请输入姓名'" v-model="state.ruleForm.name" clearable autocomplete="off"></el-input>
              </el-form-item>

              <!-- 性别 -->
              <el-form-item class="register-animation5" prop="gender">
                <el-radio-group v-model="state.ruleForm.gender">
                  <el-radio :label="1">男</el-radio>
                  <el-radio :label="2">女</el-radio>
                </el-radio-group>
              </el-form-item>

              <!-- 提交按钮 -->
              <el-form-item class="register-animation7">
                <el-row gutter="20">
                  <el-col :span="12">
                    <el-button type="primary" class="register-content-submit" round @click="registerClick">
                      <span>提交</span>
                    </el-button>
                  </el-col>
                  <el-col :span="12">
                    <el-button type="text" class="register-content-submit" round @click="goToLogin">
                      <span>返回登录</span>
                    </el-button>
                  </el-col>
                </el-row>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>

    <div class="register-authorization z-10">
    </div>
  </div>

  <div v-if="siteBg">
    <img :src="siteBg" class="fixed inset-0 z-1 w-full h-full" />
  </div>
</template>

<script lang="ts">
import { reactive, defineComponent, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import * as registerApi from '/@/views/system/register/api'; // 注册API接口

export default defineComponent({
  name: 'registerAccount',
  setup() {
    const router = useRouter();

    // 初始化表单数据
    const state = reactive({
      ruleForm: {
        username: '', // 用户名
        password: '', // 密码
        email: '',    // 邮箱
        mobile: '',    // 手机号
        gender: 1,    // 性别 (1: 男, 2: 女)
        name: '',     // 姓名
      },
      loading: {
        register: false,
      },
    });

    // 表单校验规则
    const rules = reactive({
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
      ],
      mobile: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        // { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' },
      ],
      gender: [
        { required: true, message: '请选择性别', trigger: 'change' },
      ],
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
      ],
    });

    // 获取表单引用
    const formRef = ref();

    // 注册请求
    const registerClick = async () => {
      if (!formRef.value) return;

      // 验证表单
      await formRef.value.validate((valid: any) => {
        if (valid) {
          registerApi.register({
            username: state.ruleForm.username,
            password: state.ruleForm.password,  // 使用加密算法
            email: state.ruleForm.email,
            mobile: state.ruleForm.mobile,
            gender: state.ruleForm.gender,
            name: state.ruleForm.name,
            dept_belong_id: 1,  // 固定为1
            role: [1],  // 固定角色为1
          }).then((res: any) => {
            if (res.code === 2000) {
              ElMessage.success('注册成功');
              router.push('/login');  // 注册成功后跳转到登录页
            }
          }).catch((err: any) => {
            ElMessage.error('注册失败，请稍后再试');
          });
        } else {
          ElMessage.error("请填写完整注册信息");
        }
      });
    };

    // 返回登录
    const goToLogin = () => {
      router.push('/login'); // 点击返回登录按钮时跳转到登录页面
    };

    return {
      formRef, // 返回formRef
      registerClick,
      goToLogin,
      state,
      rules,
    };
  },
});
</script>

<style scoped lang="scss">
.register-container {
  height: 100vh; /* 使用视口高度确保全屏 */
  background: var(--el-color-white);
  background-image: url('/@/assets/image.png'); /* 替换为新的背景图片路径 */
  background-size: cover; /* 使背景图片覆盖整个容器 */
  background-position: center; /* 将背景图片居中 */
  background-repeat: no-repeat; /* 防止背景图片重复 */
  display: flex;
  flex-direction: column; /* 垂直布局 */
  align-items: center; /* 垂直居中 */
  justify-content: flex-start; /* 改为顶部对齐 */
  position: relative; /* 确保背景图片在容器内 */
  padding-left: 50px; /* 向左移动一些 */

  /* 新增标题样式 */
  .register-title {
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

  .register-right {
    width: 500px;
    position: absolute;
    right: 100px; /* 添加此行，将表单移到右侧 */
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
    z-index: 2;
    margin-top: 150px;

    .register-right-warp {
      border: 1px solid var(--el-color-primary-light-3);
      border-radius: 10px;
      width: 100%;
      height: 500px;
      position: relative;
      overflow: hidden;
      background-color: rgba(255, 255, 255, 0.7);

      .register-right-warp-one,
      .register-right-warp-two {
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

      .register-right-warp-one {
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

      .register-right-warp-two {
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

      .register-right-warp-main {
        display: flex;
        flex-direction: column;
        height: 500px;


        .register-right-warp-main-title {
          height: 80px;
          line-height: 130px;
          font-size: 20px;
          text-align: center;
          letter-spacing: 3px;
          animation: logoAnimation 0.3s ease;
          animation-delay: 0.3s;
          color: var(--el-text-color-primary);
          margin-top: 0px; 
        }

        .register-right-warp-main-form {
          flex: 1;
          padding: 0 50px 50px;
          height: 100px;
        }
      }
    }
  }

  .register-authorization {
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
