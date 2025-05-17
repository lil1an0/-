import * as api from './api';
import { dict, UserPageQuery, AddReq, DelReq, EditReq, compute, CreateCrudOptionsProps, CreateCrudOptionsRet } from '@fast-crud/fast-crud';
import { dictionary } from '/@/utils/dictionary';
import { successMessage } from '/@/utils/message';
import { auth } from '/@/utils/authFunction';
import tableSelector from '/@/components/tableSelector/index.vue';
import { shallowRef } from 'vue';

export const createCrudOptions = function ({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
	const pageRequest = async (query: UserPageQuery) => {
		return await api.GetList(query);
	};
	const editRequest = async ({ form, row }: EditReq) => {
		form.id = row.id;
		return await api.UpdateObj(form);
	};
	const delRequest = async ({ row }: DelReq) => {
		return await api.DelObj(row.id);
	};
	const addRequest = async ({ form }: AddReq) => {
		return await api.AddObj(form);
	};

	/**
	 * 懒加载
	 * @param row
	 * @returns {Promise<unknown>}
	 */
	const loadContentMethod = (tree: any, treeNode: any, resolve: Function) => {
		pageRequest({ pcode: tree.code }).then((res: APIResponseData) => {
			resolve(res.data);
		});
	};

	return {
		crudOptions: {
			request: {
				pageRequest,
				addRequest,
				editRequest,
				delRequest,
			},
			actionbar: {
				buttons: {
					add: {
						show: auth('area:Create'),
					},
				},
			},
			rowHandle: {
				//固定右侧
				fixed: 'right',
				width: 200,
				buttons: {
					view: {
						show: false,
					},
					edit: {
						iconRight: 'Edit',
						type: 'text',
						show: auth('area:Update'),
					},
					remove: {
						iconRight: 'Delete',
						type: 'text',
						show: auth('area:Delete'),
					},
				},
			},
			pagination: {
				show: false,
			},
			table: {
				rowKey: 'id',
				lazy: true,
				load: loadContentMethod,
				treeProps: { children: 'children', hasChildren: 'hasChild' },
			},
			columns: {
				_index: {
					title: '序号',
					form: { show: false },
					column: {
						type: 'index',
						align: 'center',
						width: '70px',
						columnSetDisabled: true, //禁止在列设置中选择
					},
				},
				sales_date: {
					title: '销售日期',
					search: {
						show: true,
					},
					treeNode: true,
					type: 'input',
					column: {
						minWidth: 120,
					},
					form: {
						component: {
							placeholder: '请输入名称',
						},
					},
				},
				store_style: {
					title: '店风格',
					search: {
						disabled: true,
					},
					width: 130,
					type: 'table-selector',
					column: {
						show: false,
					},
					form: {
						component: {
							placeholder: '请输入店风格',
						},
					},
				},
				store_name: {
					title: '店名',
					search: {
						show: true,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
					form: {
						component: {
							placeholder: '请输入店名',
						},
					},
				},
				category_description: {
					title: '品类描述',
					search: {
						show: true,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
					form: {
						component: {
							placeholder: '请输入品类描述',
						},
					},
				},
				brand_description: {
					title: '品牌描述',
					search: {
						show: true,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
					form: {
						component: {
							placeholder: '请输入品牌描述',
						},
					},
				},
				region: {
					title: '所属大区',
					search: {
						show: true,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
					form: {
						component: {
							placeholder: '请输入所属大区',
						},
					},
				},
				sub_region: {
					title: '所属小区',
					search: {
						show: true,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
					form: {
						component: {
							placeholder: '请输入所属小区',
						},
					},
				},
				sales_amount: {
					title: '销售额',
					search: {
						show: false,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
				},
				gross_profit: {
					title: '毛利',
					search: {
						show: false,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
				},
				gross_profit_margin: {
					title: '毛利率',
					search: {
						show: false,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
				},
			},
		},
	};
};
