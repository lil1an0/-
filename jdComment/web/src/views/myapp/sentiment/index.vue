<template>
	<div class="home-container">
		<el-row :gutter="15" class="home-card-two mb15">
			<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
				<div class="home-card-item">
					<div style="height: 100%" ref="homeLineRef"></div>
				</div>
			</el-col>
		</el-row>
		<el-row :gutter="15" class="home-card-two mb15">
			<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
				<div class="home-card-item">
					<div style="height: 100%" ref="homeBarRef"></div>
				</div>
			</el-col>
		</el-row>
		<el-row :gutter="15" class="home-card-two mb15">
			<el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
				<div class="home-card-item">
					<div style="height: 100%" ref="predictionRef"></div>
				</div>
			</el-col>
		</el-row>
		<el-row :gutter="15" class="home-card-two mb15">
			<el-col :xs="24" :sm="8" :md="8" :lg="8" :xl="8">
				<div class="home-card-item">
					<div style="height: 100%" ref="homeBarRef1"></div>
				</div>
			</el-col>
			<el-col :xs="24" :sm="8" :md="8" :lg="8" :xl="8">
				<div class="home-card-item">
					<div style="height: 100%" ref="homeBarRef3"></div>
				</div>
			</el-col>
			<el-col :xs="24" :sm="8" :md="8" :lg="8" :xl="8">
				<div class="home-card-item">
					<div style="height: 100%" ref="homeBarRef2"></div>
				</div>
			</el-col>
		</el-row>
	</div>
</template>


<script lang="ts">
import { toRefs, reactive, defineComponent, onMounted, ref, watch, nextTick, onActivated } from 'vue';
import * as echarts from 'echarts';
import 'echarts-wordcloud';
import axios from 'axios';
import { storeToRefs } from 'pinia';
import { useThemeConfig } from '/@/stores/themeConfig';
import { useTagsViewRoutes } from '/@/stores/tagsViewRoutes';
import * as api from './api';
import { UserPageQuery } from '@fast-crud/fast-crud';
import { data } from 'autoprefixer';

let global: any = {
	homeChartOne: null,
	homeChartTwo: null,
	homeChartThree: null,
	homeChartFour: null,
	homeChartFive: null,
	homeChartSix: null,
	dispose: [null, '', undefined],
};

export default defineComponent({
	name: 'home',
	setup() {
		const homeLineRef = ref();
		const homeBarRef = ref();
		const homeBarRef1 = ref();
		const homeBarRef2 = ref();
		const homeBarRef3 = ref();
		const predictionRef = ref();
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

		// 折线图
		const initLineChart = (result: any[]) => {
			if (global.homeChartOne && !global.dispose.includes(global.homeChartOne)) {
				global.homeChartOne.dispose();
			}
			global.homeChartOne = echarts.init(homeLineRef.value, state.charts.theme);

			const option = {
				title: {
					text: '情感饼图',
					left: 'left'
				},
				tooltip: {
					trigger: 'item'
				},
				legend: {
					// orient: 'vertical',
					left: 'center'
				},
				series: [
					{
					name: 'Access From',
					type: 'pie',
					radius: '50%',
					data: result,
					emphasis: {
						itemStyle: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.5)'
						}
					}
					}
				]
			};
			global.homeChartOne.setOption(option);
			state.myCharts.push(global.homeChartOne);
		};

		// 柱状图
		const initBarChart = (result: any) => {
			if (global.homeChartTwo && !global.dispose.includes(global.homeChartTwo)) {
				global.homeChartTwo.dispose();
			}
			global.homeChartTwo = echarts.init(homeBarRef.value, state.charts.theme);


			console.log("result");
			console.log(result.data[0]);

			const option = {
				title: {
					text: '每天正负向情感折线趋势图'
				},
				tooltip: {
					trigger: 'axis',
					axisPointer: {
						type: 'cross'
					}
				},
				legend: {
					data: ['好评', '中评', '差评']
				},
				grid: {
					left: '3%',
					right: '4%',
					bottom: '3%',
					containLabel: true
				},
				toolbox: {
					feature: {
						saveAsImage: {}
					}
				},
				xAxis: {
					type: 'category',
					boundaryGap: false,
					data: result.columns
				},
				yAxis: [
					{
						type: 'value',
						name: '好评数量',
						position: 'left',
						axisLabel: {
							formatter: '{value}'
						}
					},
					{
						type: 'value',
						name: '中差评数量',
						position: 'right',
						axisLabel: {
							formatter: '{value}'
						}
					}
				],
				series: [
					{
						name: '好评',
						type: 'line',
						yAxisIndex: 0,
						data: result.data[0],
						itemStyle: {
							color: '#91cc75'
						}
					},
					{
						name: '中评',
						type: 'line',
						yAxisIndex: 1,
						data: result.data[1],
						itemStyle: {
							color: '#fac858'
						}
					},
					{
						name: '差评',
						type: 'line',
						yAxisIndex: 1,
						data: result.data[2],
						itemStyle: {
							color: '#ee6666'
						}
					}
				]
			};
			global.homeChartTwo.setOption(option);
			state.myCharts.push(global.homeChartTwo);
		};


		const initBarChart1 = (result: any) => {
			if (global.homeChartThree && !global.dispose.includes(global.homeChartThree)) {
				global.homeChartThree.dispose();
			}
			global.homeChartThree = echarts.init(homeBarRef1.value, state.charts.theme);
			console.log(result);
			const option = {
				title: { text: '好评词云图' },
				tooltip: {},
				series: [
					{
					type: 'wordCloud',
					sizeRange: [12, 60],  // 字体大小范围
					rotationRange: [0, 0],  // 不旋转
					shape: 'circle',  // 词云图形状
					width: '100%',
					height: '100%',
					gridSize: 8,  // 网格大小
					drawOutOfBound: false,  // 不绘制超出范围的单词
					data: result,  // 数据
					textStyle: {
						fontFamily: 'Arial, sans-serif',  // 字体
						fontWeight: 'bold',  // 字体加粗
						color: function () {
						return 'rgb(' + [
							Math.round(Math.random() * 255),
							Math.round(Math.random() * 255),
							Math.round(Math.random() * 255)
						].join(',') + ')';  // 随机颜色
						}
					}
					}
				]
			};
			global.homeChartThree.setOption(option);
			state.myCharts.push(global.homeChartThree);
		};


		const initBarChart2 = (result: any) => {
			if (global.homeChartFour && !global.dispose.includes(global.homeChartFour)) {
				global.homeChartFour.dispose();
			}
			global.homeChartFour = echarts.init(homeBarRef2.value, state.charts.theme);

			const option = {
				title: { text: '差评词云图' },
				tooltip: {},
				series: [
					{
					type: 'wordCloud',
					sizeRange: [12, 60],  // 字体大小范围
					rotationRange: [0, 0],  // 不旋转
					shape: 'circle',  // 词云图形状
					width: '100%',
					height: '100%',
					gridSize: 8,  // 网格大小
					drawOutOfBound: false,  // 不绘制超出范围的单词
					data: result,  // 数据
					textStyle: {
						fontFamily: 'Arial, sans-serif',  // 字体
						fontWeight: 'bold',  // 字体加粗
						color: function () {
						return 'rgb(' + [
							Math.round(Math.random() * 255),
							Math.round(Math.random() * 255),
							Math.round(Math.random() * 255)
						].join(',') + ')';  // 随机颜色
						}
					}
					}
				]
			};
			global.homeChartFour.setOption(option);
			state.myCharts.push(global.homeChartFour);
		};


		const initBarChart3 = (result: any) => {
			if (global.homeChartFive && !global.dispose.includes(global.homeChartFive)) {
				global.homeChartFive.dispose();
			}
			global.homeChartFive = echarts.init(homeBarRef3.value, state.charts.theme);

			const option = {
				title: { text: '中评词云图' },
				tooltip: {},
				series: [
					{
					type: 'wordCloud',
					sizeRange: [12, 60],  // 字体大小范围
					rotationRange: [0, 0],  // 不旋转
					shape: 'circle',  // 词云图形状
					width: '100%',
					height: '100%',
					gridSize: 8,  // 网格大小
					drawOutOfBound: false,  // 不绘制超出范围的单词
					data: result,  // 数据
					textStyle: {
						fontFamily: 'Arial, sans-serif',  // 字体
						fontWeight: 'bold',  // 字体加粗
						color: function () {
						return 'rgb(' + [
							Math.round(Math.random() * 255),
							Math.round(Math.random() * 255),
							Math.round(Math.random() * 255)
						].join(',') + ')';  // 随机颜色
						}
					}
					}
				]
			};
			global.homeChartFive.setOption(option);
			state.myCharts.push(global.homeChartFive);
		};

		// 预测图表
		const initPredictionChart = (result: any) => {
			if (global.homeChartSix && !global.dispose.includes(global.homeChartSix)) {
				global.homeChartSix.dispose();
			}
			global.homeChartSix = echarts.init(predictionRef.value, state.charts.theme);

			// 拼接x轴
			const all_dates = [...result.history_dates, ...result.future_dates];
			// 历史真实好评率，未来为null
			const history_series = [
				...result.history_rates.map((r: number) => (r * 100).toFixed(2)),
				...Array(result.future_dates.length).fill(null)
			];
			// 未来多项式预测，历史为null
			const poly_series = [
				...Array(result.history_dates.length).fill(null),
				...result.poly_pred.map((r: number) => (r * 100).toFixed(2))
			];
			// 未来岭回归预测，历史为null
			const ridge_series = [
				...Array(result.history_dates.length).fill(null),
				...result.ridge_pred.map((r: number) => (r * 100).toFixed(2))
			];

			const option = {
				title: {
					text: '好评率未来预测',
				},
				tooltip: {
					trigger: 'axis',
					axisPointer: {
						type: 'cross'
					},
					formatter: function(params: any) {
						let result = params[0].axisValue + '<br/>';
						params.forEach((param: any) => {
							if (param.value !== null) {
								result += param.marker + param.seriesName + ': ' + param.value + '%<br/>';
							}
						});
						return result;
					}
				},
				legend: {
					data: ['实际好评率', '多项式回归预测', '岭回归预测']
				},
				grid: {
					left: '3%',
					right: '4%',
					bottom: '3%',
					containLabel: true
				},
				toolbox: {
					feature: {
						saveAsImage: {}
					}
				},
				xAxis: {
					type: 'category',
					boundaryGap: false,
					data: all_dates,
					axisLabel: {
						rotate: 45
					},
					axisPointer: {
						label: {
							show: true
						}
					}
				},
				yAxis: {
					type: 'value',
					axisLabel: {
						formatter: '{value}%'
					},
					min: 0,
					max: 100
				},
				series: [
					{
						name: '实际好评率',
						type: 'line',
						data: history_series,
						itemStyle: {
							color: '#91cc75'
						},
						lineStyle: {
							width: 2
						},
						symbol: 'circle',
						symbolSize: 6
					},
					{
						name: '多项式回归预测',
						type: 'line',
						data: poly_series,
						itemStyle: {
							color: '#5470c6'
						},
						lineStyle: {
							width: 2,
							type: 'dashed'
						},
						symbol: 'none'
					},
					{
						name: '岭回归预测',
						type: 'line',
						data: ridge_series,
						itemStyle: {
							color: '#ee6666'
						},
						lineStyle: {
							width: 2,
							type: 'dashed'
						},
						symbol: 'none'
					}
				]
			};
			global.homeChartSix.setOption(option);
			state.myCharts.push(global.homeChartSix);
		};

		// 数据获取
		const fetchData = async () => {
			try {
				const response = await api.GetList();
				initLineChart(response.result1);
				initBarChart(response.result2);
				initBarChart1(response.result3.good);
				initBarChart2(response.result3.bad);
				initBarChart3(response.result3.middle);
				initPredictionChart(response.result4);
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
			homeBarRef1,
			homeBarRef2,
			homeBarRef3,
			predictionRef,
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
			height: 450px;
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
</style>
