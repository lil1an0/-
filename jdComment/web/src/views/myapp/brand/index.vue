<template>
	<div class="home-container">
  
	  <el-row :gutter="15" class="home-card-two mb15">
		<el-col :xs="48" :sm="24" :md="24" :lg="24" :xl="24">
		  <div class="home-card-item">
			<div style="height: 100%" ref="homeLineRef"></div>
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

			// Initialize the chart instance
			global.homeChartOne = echarts.init(homeLineRef.value, state.charts.theme);


			const series = result.res_result.slice(1).map(() => ({
				type: 'line',
				smooth: true,
				seriesLayoutBy: 'row',
				emphasis: { focus: 'series' }
				}));

				// 添加饼图的配置
				series.push({
				type: 'pie',
				id: 'pie',
				radius: '30%',
				center: ['50%', '25%'],
				emphasis: {
					focus: 'self'
				},
				label: {
					formatter: '{b}: ({d}%)'
				},
				encode: {
					itemName: 'brand', // 指定用于显示名称的列
					value: '2017-03',  // 指定用于饼图数值的列
					tooltip: '2017-03' // 指定提示框的内容
				}
			});


			const option: echarts.EChartsOption = {
				legend: {},
				tooltip: {
					trigger: 'axis',
					showContent: false
				},
				dataset: {
					source: result.res_result
				},
				xAxis: { type: 'category' },
				yAxis: { gridIndex: 0 },
				grid: { top: '55%' },
				series: series
			};

			// Add the `updateAxisPointer` event listener to the correct chart instance
			global.homeChartOne.on('updateAxisPointer', function (event: any) {
				const xAxisInfo = event.axesInfo[0];
				if (xAxisInfo) {
					const dimension = xAxisInfo.value + 1;
					global.homeChartOne.setOption({
						series: [
							{
								id: 'pie',
								label: {
									formatter: `{b}: {@[${dimension}]} ({d}%)`
								},
								encode: {
									value: dimension,
									tooltip: dimension
								}
							}
						]
					});
				}
			});

			// Set the chart option
			global.homeChartOne.setOption(option);
			state.myCharts.push(global.homeChartOne);
		};



		// 数据获取
		const fetchData = async () => {
			try {
				const response = await api.GetList();
				initLineChart(response);
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
