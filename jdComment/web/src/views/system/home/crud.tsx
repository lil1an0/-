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
				show: false, // 新增这一行，隐藏顶部按钮栏
				buttons: {
					add: {
						show: auth('area:Create'),
					},
				},
			},
			toolbar: {
				show: false, // 这里是关键
			},
			rowHandle: {
				//固定右侧
				show: false, // 新增这一行，隐藏顶部按钮栏
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
				user_id: {
					title: '用户ID',
					search: {
						disabled: false,
					},
					width: 130,
					type: 'table-selector',
					column: {
						show: false,
					}
				},
				product_id: {
					title: '商品ID',
					search: {
						show: false,
					},
					type: 'input',
					column: {
						minWidth: 90,
					}
				},
				review_time: {
					title: '评论时间',
					search: {
						show: false,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
				},
				review_title: {
					title: '评论标题',
					search: {
						show: false,
					},
					type: 'input',
					column: {
						minWidth: 90,
					}
				},
				review_content: {
					title: '评论内容',
					search: {
						show: false,
					},
					type: 'input',
					column: {
						minWidth: 90,
					}
				},
				rating: {
					title: '评分',
					search: {
						show: true,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
					form: {
						component: {
							placeholder: '请输入评分',
						},
					},
				},
				label: {
					title: '评价标签',
					search: {
						show: true,
					},
					type: 'input',
					column: {
						minWidth: 90,
					},
					form: {
						component: {
							placeholder: '请输入标签',
						},
					},
				}
			},
		},
	};
};
