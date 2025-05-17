import { request } from '/@/utils/service';
import { UserPageQuery, AddReq, DelReq, EditReq, InfoReq } from '@fast-crud/fast-crud';


export const apiPrefix = '/myapp/productReview/predict/';
// export function GetList() {
// 	return request({
// 		url: apiPrefix,
// 		method: 'get',
// 	});
// }


export function predictObj(obj: AddReq) {
    return request({
        url: apiPrefix,
        method: 'post',
        data: obj,
    });
}

export function GetPermission() {
    return request({
        url: apiPrefix + '',
        method: 'get',
    });
}
