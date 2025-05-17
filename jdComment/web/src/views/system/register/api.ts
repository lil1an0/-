import { request } from "/@/utils/service";
// import { PageQuery, AddReq} from '@fast-crud/fast-crud';

export const apiPrefix = '/api/system/user/';

export function getCaptcha() {
    return request({
        url: '/api/captcha/',
        method: 'get',
    });
}
export function register(params: object) {
    return request({
        url: apiPrefix,
        method: 'post',
        data: params
    });
}

export function getUserInfo() {
    return request({
        url: '/api/system/user/user_info/',
        method: 'get',
    });
}

