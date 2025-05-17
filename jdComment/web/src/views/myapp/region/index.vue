<template>
	<div class="home-container">
		<el-row :gutter="15" class="home-card-two mb15">
			<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
				<div class="home-card-item">
					<div style="height: 100%" ref="homeLineRef"></div>
				</div>
			</el-col>
			<el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
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

		// 折线图
		const initLineChart = (result: any[]) => {
			if (global.homeChartOne && !global.dispose.includes(global.homeChartOne)) {
				global.homeChartOne.dispose();
			}
			global.homeChartOne = echarts.init(homeLineRef.value, state.charts.theme);

			const option = {
				legend: { top: 'bottom' },
				title: { text: '子区域销售额分析' },
				toolbox: {
					show: true,
					feature: {
						mark: { show: true },
						dataView: { show: true, readOnly: false },
						restore: { show: true },
						saveAsImage: { show: true },
					},
				},
				series: [
					{
						name: 'Nightingale Chart',
						type: 'pie',
						radius: [50, 250],
						center: ['50%', '50%'],
						roseType: 'area',
						itemStyle: { borderRadius: 8 },
						data: result,
					},
				],
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
				title: { text: '大区销售额分析' },
				tooltip: {
					trigger: 'axis',
					axisPointer: { type: 'shadow' },
				},
				legend: {},
				grid: {
					left: '3%',
					right: '4%',
					bottom: '3%',
					containLabel: true,
				},
				xAxis: {
					type: 'value',
					boundaryGap: [0, 0.01],
				},
				yAxis: {
					type: 'category',
					data: result.region || [],
				},
				series: [
					{
						name: '',
						type: 'bar',
						data: result.total_sales || [],
					},
				],
			};
			global.homeChartTwo.setOption(option);
			state.myCharts.push(global.homeChartTwo);
		};

		// 数据获取
		const fetchData = async () => {
			try {
				const response = await api.GetList();
				const barResponse = await api.GetBarList();
				initLineChart(response);
				initBarChart(barResponse);
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
</style>
