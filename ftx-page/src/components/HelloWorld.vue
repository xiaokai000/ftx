<template>
  <div>
      <el-select v-model="value" placeholder="请选择省份">
        <el-option
          v-for="item in provinces"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>

      <el-select v-model="value" placeholder="请选择城市">
        <el-option
          v-for="item in citys"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>

      <el-date-picker
      v-model="value1"
      type="daterange"
      range-separator="至"
      start-placeholder="开始日期"
      end-placeholder="结束日期">
      </el-date-picker>

      <div id="myChart" :style="{width: '300px', height: '300px'}"></div>
    </div>

</template>

<script>
  export default {
    data() {
      return {
        provinces: [{
          value: '选项1',
          label: '黄金糕'
        }],
        value: '',
        value1: '',
        new_house_price_list: []
      };
    },
    mounted(){
      this.drawLine();
  },
    methods: {
      drawLine(){

          let that = this;
            axios.post('http://127.0.0.1:5000/')
            .then(function(response){
                that.new_house_price_list = response.data.new_house_price_list
            })



          // 基于准备好的dom，初始化echarts实例
          let myChart = this.$echarts.init(document.getElementById('myChart'))
          // 绘制图表
          myChart.setOption({
              title: { text: '在Vue中使用echarts' },
              tooltip: {},
              xAxis: {
                  data: []
              },
              yAxis: {},
              series: [{
                  name: '销量',
                  type: 'bar',
                  data: this.new_house_price_list
              }]
          });
    }
  }
  };
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
