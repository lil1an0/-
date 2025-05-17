import { request } from '/@/utils/service';
import { UserPageQuery, AddReq, DelReq, EditReq, InfoReq } from '@fast-crud/fast-crud';


export const apiPrefix = '/myapp/salesRecords/sub_region_sales_ranking/';
export const apiBarPrefix = '/myapp/salesRecords/region_sales_ranking/';
export function GetList() {
	return request({
		url: apiPrefix,
		method: 'get',
	});
}


export function GetBarList() {
	return request({
		url: apiBarPrefix,
		method: 'get',
	});
}

export function GetPermission() {
    return request({
        url: apiPrefix + '',
        method: 'get',
    });
}
