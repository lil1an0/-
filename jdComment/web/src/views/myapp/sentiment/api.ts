import { request } from '/@/utils/service';
import { UserPageQuery, AddReq, DelReq, EditReq, InfoReq } from '@fast-crud/fast-crud';


export const apiPrefix = '/myapp/productReview/get_sentiment/';
export function GetList() {
	return request({
		url: apiPrefix,
		method: 'get',
	});
}


export function GetPermission() {
    return request({
        url: apiPrefix + '',
        method: 'get',
    });
}
