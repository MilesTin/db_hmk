<template>
  <div @click="showDetail()" class="newList-main">
    <el-card :body-style="{ padding: '0px' }">
      <el-image :src="list.pics[0].pic">
        <div slot="placeholder" class="image-slot">
          加载中<span class="dot">...</span>
        </div>
      </el-image>
      <!-- {{list.pics[0].pic}} -->
      <!-- <p>这里是一个商品</p> -->
      <div style="padding: 5px; text-align: left;">
        <span style="font-weight: bold;">{{ list.name }}</span>

        <div class="price">￥{{ list.price }}</div>

        <div class="time">{{ list.stuId }} 发布于{{ list.publish_time }}</div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'newList',
  props: {
    list: Object
  },
  data () {
    return {
      //占位图URL
      placeholderChart: ''
    }
  },
  computed: {
    
  },
  created () {
    //生成占位图
    console.log('new list created')
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    const m = this.list.first_img_width_height.split('/')
    canvas.width = Number(m[0])
    canvas.height = Number(m[1])
    ctx.fillStyle = '#e0e0e0'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    this.placeholderChart = canvas.toDataURL()
  },
  methods: {
    showDetail () {
      window.localStorage.setItem('detail', JSON.stringify(this.list))
      this.$router.push('/detail')
    }
  }
}
</script>

<style scoped>
.el-card {
  margin-top: 6px;
  border-radius: 10px;
}
.time {
  font-size: 13px;
  color: #999;
  text-align: right;
  float: right;
  border-top: 0.5px solid #e5e5e5;
  width: 100%;
  padding-top: 5px;
  padding-bottom: 5px;
}

.price {
  padding-top: 5px;
  padding-bottom: 5px;
  /*float: right;*/
  color: #ff0000;
  font-weight: bold;
  text-align: left;
}

/* .image {
    width: 100%;
    display: block;
  } */
</style>
