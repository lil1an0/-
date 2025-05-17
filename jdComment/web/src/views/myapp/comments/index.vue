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
					<div style="height: 100%" ref="homeBarRef1"></div>
				</div>
			</el-col>
		</el-row>
		<el-row :gutter="15" class="home-card-two mb15">
			<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
				<div class="home-card-item">
					<div style="height: 100%" ref="homeBarRef2"></div>
				</div>
			</el-col>
			<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
				<div class="home-card-item">
					<div style="height: 100%" ref="homeBarRef3"></div>
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
					text: '每日评价趋势图'
				},
				tooltip: {
					trigger: 'axis'
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
					data: result.date
				},
				yAxis: {
					type: 'value'
				},
				series: [
					{
						name: '评论数',
						type: 'line',
						stack: 'Total',
						data: result.counts
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
			const option = {
				title: {
					text: '词评前20词评图',
				},
				tooltip: {
					trigger: 'axis'
				},
				legend: {
					data: ['Rainfall', 'Evaporation']
				},
				toolbox: {
					show: true,
					feature: {
					dataView: { show: true, readOnly: false },
					magicType: { show: true, type: ['line', 'bar'] },
					restore: { show: true },
					saveAsImage: { show: true }
					}
				},
				calculable: true,
				xAxis: [
					{
					type: 'category',
					// prettier-ignore
					data: result.columns
					}
				],
				yAxis: [
					{
					type: 'value'
					}
				],
				series: [
					{
					name: '',
					type: 'bar',
					data: result.data,
					itemStyle: {
						color: '#FF6347'  // 设置条形图的颜色，这里使用的是番茄红
					},
					markPoint: {
						data: [
						{ type: 'max', name: 'Max' },
						{ type: 'min', name: 'Min' }
						]
					},
					markLine: {
						data: [{ type: 'average', name: 'Avg' }]
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
			const option = {
				title: { text: '词云图' },
				tooltip: {},
				series: [
					{
						type: 'wordCloud',
						shape: 'cardinal',  // 使用矩形形状
						sizeRange: [20, 120],  // 增加字体大小范围
						gridSize: 2,  // 减小网格间距
						width: '100%',  // 确保填满画布宽度
						height: '100%',  // 确保填满画布高度
						rotationRange: [0, 0],  // 水平排列单词
						drawOutOfBound: false,  // 不绘制出界单词
						textStyle: {
							fontFamily: 'Arial, sans-serif',
							fontWeight: 'bold',
							color: function () {
								return 'rgb(' + [
									Math.round(Math.random() * 255),
									Math.round(Math.random() * 255),
									Math.round(Math.random() * 255)
								].join(',') + ')';
							}
						},
						data: result // 替换为你的数据
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
				title: {
					text: '会员比例图',
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
			global.homeChartFour.setOption(option);
			state.myCharts.push(global.homeChartFour);
		};


		const initBarChart3 = (result: any) => {
			if (global.homeChartFive && !global.dispose.includes(global.homeChartFive)) {
				global.homeChartFive.dispose();
			}
			global.homeChartFive = echarts.init(homeBarRef3.value, state.charts.theme);

			const option = {
				title: {
					text: '商品属性饼图',
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
			global.homeChartFive.setOption(option);
			state.myCharts.push(global.homeChartFive);
		};


		// 数据获取
		const fetchData = async () => {
			try {
				const response = await api.GetList();
				initLineChart(response.result1);
				initBarChart(response.result2);
				initBarChart1(response.result3);
				initBarChart2(response.result4);
				initBarChart3(response.result5);
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
