import * as url from './urlConfig'
import axios from 'axios'

/**
 * 用户相关操作
 */
export const usersApi = {
  login(param) {
    let formData = new FormData();
    console.log(Object.keys(param))
    console.log(param)
    formData.append('stuId', param['stuId']);
    formData.append('password', param['password']);
    
    // Object.keys(param).forEach(x => {
    //   console.log(param[x])
    //   console.log(x)
    //   formData.append(String(x), param[x]);

    // })
    console.log(formData)
    return fetch(url.login, {
      method: 'POST',
      body: formData
    }).then(res=>res.json()) 
    .then(res => {
      console.log(res);
      return res;
    })
    
    // return axios.post(url.login, param, {withCredentials: true}).then((response) => {
      
    //   return response;
    // })

  },
  register(param) {
    console.log('param', param)
    return axios.post(url.register, param).then((response) => {
      return response.data
    })
  },
  getImgUploadToken(param) {
    return axios.post(
      url.getImgUploadToken, 
      param, 
      {
        // headers:{
        //   'Authorization':`token ${window.localStorage.getItem('token')}`
        // }
      }).then((response) => {
      return response.data
    })
  },
  changeAvatar(param) {
    return axios.post(
      url.changeAvatar,
      param,
      {
        headers:{
          'Authorization':`token ${window.localStorage.getItem('token')}`
        }
      }).then((response) => {
        return response.data
    })
  },
  changePassword(param) {
    return axios.post(
      url.changePassword,
      param,
      {
        headers:{
          'Authorization':`token ${window.localStorage.getItem('token')}`
        }
      }).then((response) => {
        return response.data
    })
  },
}

/**
 * 商品相关操作
 */
export const productApi = {
  getList(index) {
    return axios.get(
      `${url.getList}`, 
      {
        headers:{
          // 'Authorization':`token ${window.localStorage.getItem('token')}`
        }
      }).then((response) => {
        console.log(response)
      return response;
    })
  },
  search(key,imdex) {
    return axios.get(
      `${url.search}${key}`,{withCredentials: true}
      /*,{
        headers:{
          'Authorization':`token ${window.localStorage.getItem('token')}`
        }
      }
      */).then((response) => {
      console.log(response)
      return response.data
    })
  },
  publish(param) {
    return axios.post(
      url.publish, 
      param, 
      {
        headers:{
          'Authorization':`token ${window.localStorage.getItem('token')}`
        },
        withCredentials: true
      }).then((response) => {
      return response.data
    })
  },
  getMyPublishList(param) {
    return fetch(url.getMyPublishList, {
      method: "GET",
      credentials: "include",
      withCredentials: "true"
    }).then((response) => {
      console.log(response)
      return response;
    })


    return axios.get(
      url.getMyPublishList, {withCredentials: true},
      // {
      //   headers:{
      //     'Authorization':`token ${window.localStorage.getItem('token')}`,
      //   }
      // }
      ).then((response) => {
        console.log(response.data)
        return response.data
    })
  },
}

/**
 * 收藏相关操作
 */
export const collectApi = {
  changeCollectState(param) {
    return axios.post(
      url.changeCollectState,
      param,
      {
        headers:{
          'Authorization':`token ${window.localStorage.getItem('token')}`
        }
      }).then((response) => {
        return response.data
      })
  },
  getCollectionList() {
    return axios.get(
      url.getCollectionList, 
      {
        headers:{
          'Authorization':`token ${window.localStorage.getItem('token')}`
        }
      }).then((response) => {
      return response.data
    })
  }
}