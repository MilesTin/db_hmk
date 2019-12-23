<template>
  <div class="main">
    <v-header :headerMsg="headerMsg"></v-header>
    <el-row type="flex" justify="center">
      <el-col :xs="17" :sm="9" :md="7" :lg="5">
        <el-steps :active="active" finish-status="success" align-center>
          <el-step title="学生认证"></el-step>
          <el-step title="账户注册"></el-step>
          <!-- <el-step title="提交成功"></el-step> -->
        </el-steps>
      </el-col>
    </el-row>

    <div class="step1" v-if="active === 0">
      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-input
            placeholder="您的学号"
            prefix-icon="el-icon-user"
            v-model="stuId"
            clearable
          >
          </el-input>
        </el-col>
      </el-row>
      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-input
            placeholder="输入密码"
            prefix-icon="el-icon-view"
            v-model="password1"
            type="password"
            clearable
          ></el-input>
        </el-col>
      </el-row>

      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-input
            placeholder="确认密码"
            prefix-icon="el-icon-view"
            v-model="password2"
            type="password"
            clearable
          ></el-input>
        </el-col>
      </el-row>

      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-button
            type="primary"
            @click="next()"
            :disabled="!password1 || !stuId || !password2"
            >下一步</el-button
          >
        </el-col>
      </el-row>
    </div>

    <div class="step2" v-if="active === 1" v-loading="registering">
      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-input
            placeholder="请输入邮箱"
            prefix-icon="el-icon-message"
            type="email"
            v-model="email"
            clearable
          ></el-input>
        </el-col>
      </el-row>
      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-input
            placeholder="请输入手机号"
            prefix-icon="el-icon-mobile-phone"
            v-model="phone"
            clearable
          ></el-input>
        </el-col>
      </el-row>
      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-input
            placeholder="您的学院"
            prefix-icon="el-icon-school"
            v-model="campus"
            clearable
          ></el-input>
              
          <!-- <el-input v-model="value" placeholder="请选择学院" prefix-icon="el-icon-school">
            <el-select v-model="value" filterable >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
          </el-input> -->
          
        </el-col>
      </el-row>
      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-input
            placeholder="您的班级"
            prefix-icon="el-icon-reading"
            v-model="class_num"
            clearable
          ></el-input>
        </el-col>
      </el-row>
      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <el-button
            type="primary"
            @click="register()"
            :disabled="!email || !campus || !phone || !class_num"
            >注册</el-button
          >
        </el-col>
      </el-row>
    </div>

    <!-- <div class="step3" v-if="active === 2">
      <el-row type="flex" justify="center">
        <el-col :xs="17" :sm="9" :md="7" :lg="5">
          <span>提交成功！待您提交的信息审核通过以后，我们会以邮件的形式通知您，请注意查收。</span>
        </el-col>
      </el-row>
    </div> -->
    <!-- <v-loading :errorMsg="submitErrorMsg"></v-loading> -->
    <!-- {{watchImgState}} -->
  </div>
</template>

<script>
import imgUpload from '@/components/imgUpload'
import myHeader from '@/components/header'
import myLoading from '@/components/loading'
import { mapGetters, mapActions, mapMutations } from 'vuex'
export default {
  name: 'register',
  components: {
    'v-upload': imgUpload,
    'v-header': myHeader
    // "v-loading": myLoading
  },
  data () {
    return {
      headerMsg: {
        centerWord: '注册',
        //这种绑定的图片只能放在static文件夹下
        leftImg: '/static/images/back.png'
      },
      stuId: '1',
      password1: '1',
      password2: '1',
      nickname: '1',
      email: '1',
      phone: '1',
      class_num: '1',
      campus: '1',
      loading: false,
      active: 0,
      loading: false,
      // value: '1',
      
      submitErrorMsg: '提交失败'
    }
  },
  computed: {
    ...mapGetters(['errorRegister', 'hasRegister', 'registering','publishState'])
  },
  methods: {
    ...mapActions([
      'actionRegister',
      
      'actionPublishError',
      'actionClearImgInfo'
    ]),
    ...mapMutations([ 'notPublish', 'publishing']),
    next () {
      if (this.checkMessage()) {
        this.active++
      }
    },
    //注册前检查用户填写的信息
    checkMessage: function () {
      if (this.password1 !== this.password2) {
        this.$message({
          message: '两次密码不一致',
          center: true,
          type: 'warning'
        })
        return false
      }
      return true
    },

    //注册
    register: function () {
      // this.registering(true)
      let obj = {
        // actual_name: this.actualName,
        stuId: this.stuId,
        nickname: this.nickname,
        password: this.password1,
        campus: this.campus,
        class_num: this.class_num,
        phone: this.phone,
        // email: this.email
      }
      this.actionRegister(obj)
      this.publishing()
      console.log('adf')
      

      //将发布状态设为发布中，开启加载界面
    },
    headerLeft: function () {
      if (this.active === 0) {
        history.back()
      } else {
        this.active--
      }
    },
    // 加载成功以后执行的操作，和loading组件配合使用
    afterLoading () {
      清空存在vuex里的图片信息
      this.actionClearImgInfo()
      将发布状态设为未发布状态
      this.notPublish()
    }
  },
  watch: {
    errorRegister () {
      if (this.errorRegister) {
        this.$message.error(this.errorRegister)
      }
    },
    hasRegister () {
      if (this.hasRegister) {
        this.active = 2
      }
    }
  }
}
</script>

<style scoped>
.main {
  width: 100%;
}
.block {
  height: 50px;
}
.upload {
  color: rgb(0, 0, 0);
  font-size: 15px;
  float: left;
  margin-bottom: 5px;
  width: 100%;
  text-align: center;
}
.el-row {
  margin-top: 30px;
}
.title {
  color: #409eff;
  font-size: 40px;
}
.el-button {
  width: 100%;
}
.remind {
  font-size: 15px;
  float: left;
  /* margin-top: 20px;*/
  color: #b22222;
}
.tips {
  margin-top: 20px;
}
/*.el-step__title.is-process {
  font-weight: 300;
  color: #303133;
  font-size: 13px;
}
.el-step_icon {
  height: 20px;
  width: 20px;
}*/
</style>
