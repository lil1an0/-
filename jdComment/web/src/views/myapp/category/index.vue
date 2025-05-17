<template>
	<div class="home-container">  
	  <el-row :gutter="15" class="home-card-two mb15">
		<el-col :xs="48" :sm="24" :md="24" :lg="24" :xl="24">
		  <div class="home-card-item">
			<div style="height: 100%" ref="homeLineRef"></div>
		  </div>
		</el-col>
	  </el-row>

	  <el-row :gutter="15" class="home-card-two mb15">
		<el-col :xs="48" :sm="24" :md="24" :lg="24" :xl="24">
		  <div class="home-card-item">
			<div style="height: 100%" ref="homeBarRef"></div>
		  </div>
		</el-col>
	  </el-row>

	</div>
  </template>


<script lang="ts">
import { toRefs, reactive, defineComponent, onMounted, ref, watch, nextTick, onActivated } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';
import { useTagsViewRoutes } from '/@/stores/tagsViewRoutes';
import * as api from './api';
import { UserPageQuery } from '@fast-crud/fast-crud';

let global: any = {
	homeChartOne: null,
	homeChartTwo: null,
	dispose: [null, '', undefined],
};

export default defineComponent({
	name: 'home',
	setup() {
		const homeLineRef = ref();
		const homeBarRef = ref();
		const storesTagsViewRoutes = useTagsViewRoutes();
		const storesThemeConfig = useThemeConfig();
		const { themeConfig } = storeToRefs(storesThemeConfig);
		const { isTagsViewCurrenFull } = storeToRefs(storesTagsViewRoutes);
		const state = reactive({
			myCharts: [],
			charts: {
				theme: '',
				bgColor: '',
				color: '#303133',
			},
		});
		const selectedCategory = ref('电子产品'); 
    	const categories = ref(['电子产品', '家居用品', '服饰', '食品', '玩具']);

		// 折线图
		const initLineChart = (result: any[]) => {
			if (global.homeChartOne && !global.dispose.includes(global.homeChartOne)) {
				global.homeChartOne.dispose();
			}
			global.homeChartOne = echarts.init(homeLineRef.value, state.charts.theme);

			const option = {
				title: { text: '品类销售额度变化趋势' },
				xAxis: {
					type: 'category',
					data: result.columns  // X轴上的分类
				},
				yAxis: {
					type: 'value'  // Y轴为数值类型
				},
				series: result.data,
				legend: {
					right: 0,  // 将图例放置在右侧
					top: 'middle',  // 将图例放置在顶部
					orient: 'verticle',  // 图例横向排列
					align: 'left'  // 图例对齐方式
				},
				tooltip: {
					trigger: 'axis',  // 鼠标悬停时触发的区域，可以是 'item' 或 'axis'
					formatter: function (params) {
					let tooltipHtml = '';  // 用于存放 tooltip 中的内容
					params.forEach(function (param) {
						tooltipHtml += `${param.seriesName}: ${param.value}<br/>`;  // 展示每条线的名称和值
					});
					return tooltipHtml;  // 返回格式化后的内容
					}
				}
			};

			global.homeChartOne.setOption(option);
			state.myCharts.push(global.homeChartOne);
		};


		const initBarChart = (result: any) => {
			if (global.homeChartTwo && !global.dispose.includes(global.homeChartTwo)) {
				global.homeChartTwo.dispose();
			}
			global.homeChartTwo = echarts.init(homeBarRef.value, state.charts.theme);

			const option = {
				title: { text: '品类毛利变化趋势' },
				xAxis: {
					type: 'category',
					data: result.columns  // X轴上的分类
				},
				yAxis: {
					type: 'value'  // Y轴为数值类型
				},
				series: result.gross_profit,
				legend: {
					right: 0,  // 将图例放置在右侧
					top: 'middle',  // 将图例放置在顶部
					orient: 'verticle',  // 图例横向排列
					align: 'left'  // 图例对齐方式
				},
				tooltip: {
					trigger: 'axis',  // 鼠标悬停时触发的区域，可以是 'item' 或 'axis'
					formatter: function (params) {
					let tooltipHtml = '';  // 用于存放 tooltip 中的内容
					params.forEach(function (param) {
						tooltipHtml += `${param.seriesName}: ${param.value}<br/>`;  // 展示每条线的名称和值
					});
					return tooltipHtml;  // 返回格式化后的内容
					}
				}
			};
			global.homeChartTwo.setOption(option);
			state.myCharts.push(global.homeChartTwo);
		};

		// 数据获取
		const fetchData = async () => {
			try {
				const response = await api.GetList();
				initLineChart(response);
				initBarChart(response);
				console.log(response.data);
				console.log(response.gross_profit);
			} catch (error) {
				console.error('Error fetching data:', error);
			}
		};

		// 图表自适应
		const initEchartsResizeFun = () => {
			nextTick(() => {
				state.myCharts.forEach((chart, index) => {
					setTimeout(() => chart.resize(), index * 1000);
				});
			});
		};

		const initEchartsResize = () => {
			window.addEventListener('resize', initEchartsResizeFun);
		};

		// 生命周期
		onMounted(() => {
			initEchartsResize();
			fetchData();
		});

		onActivated(() => {
			initEchartsResizeFun();
		});

		watch(
			() => isTagsViewCurrenFull.value,
			() => {
				initEchartsResizeFun();
			}
		);

		return {
			homeLineRef,
			homeBarRef,
			selectedCategory,
			categories,
			...toRefs(state),
		};
	},
});
</script>

<style scoped lang="scss">
$homeNavLengh: 8;
.home-container {
	overflow: hidden;
	.home-card-one,
	.home-card-two,
	.home-card-three {
		.home-card-item {
			width: 100%;
			height: 500px;
			border-radius: 4px;
			transition: all ease 0.3s;
			margin-top: 20px;
			padding: 20px;
			overflow: hidden;
			background: var(--el-color-white);
			color: var(--el-text-color-primary);
			border: 1px solid var(--next-border-color-light);
			&:hover {
				box-shadow: 0 2px 12px var(--next-color-dark-hover);
				transition: all ease 0.3s;
			}
			&-icon {
				width: 70px;
				height: 70px;
				border-radius: 100%;
				flex-shrink: 1;
				i {
					color: var(--el-text-color-placeholder);
				}
			}
			&-title {
				font-size: 15px;
				font-weight: bold;
				height: 30px;
			}
		}
	}
	.home-card-one {
		@for $i from 0 through 3 {
			.home-one-animation#{$i} {
				opacity: 0;
				animation-name: error-num;
				animation-duration: 0.5s;
				animation-fill-mode: forwards;
				animation-delay: calc($i/10) + s;
			}
		}
	}
	.home-card-two,
	.home-card-three {
		.home-card-item {
			height: 650px;
			width: 100%;
			overflow: hidden;
			.home-monitor {
				height: 100%;
				.flex-warp-item {
					width: 25%;
					height: 111px;
					display: flex;
					.flex-warp-item-box {
						margin: auto;
						text-align: center;
						color: var(--el-text-color-primary);
						display: flex;
						border-radius: 5px;
						background: var(--next-bg-color);
						cursor: pointer;
						transition: all 0.3s ease;
						&:hover {
							background: var(--el-color-primary-light-9);
							transition: all 0.3s ease;
						}
					}
					@for $i from 0 through $homeNavLengh {
						.home-animation#{$i} {
							opacity: 0;
							animation-name: error-num;
							animation-duration: 0.5s;
							animation-fill-mode: forwards;
							animation-delay: calc($i/10) + s;
						}
					}
				}
			}
		}
	}
}
.category-select {
  width: 100%;  /* 让下拉框占满整行 */
//   max-width: 600px; /* 设置最大宽度，避免过宽 */
  padding: 10px;
  font-size: 14px;
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: #fff;
  color: #555;
  cursor: pointer;
  transition: border 0.3s ease;
  margin-top: 20px;  /* 调整下拉框与顶部的距离 */
}

</style>
