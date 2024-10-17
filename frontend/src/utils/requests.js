import axios from 'axios';
import routes from './routes';

const getMessages = async (accessToken) => {
  const response = await axios.get(routes.messagesPath, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return response.data;
};

const loginUser = async (values) => {
  const params = new URLSearchParams();
  params.append('username', values.email);
  params.append('password', values.password);
  return axios.post(routes.loginPath, params);
};

const signupUser = async (values) => {
  console.log('func in')
  const form = new FormData();
  form.append('username', values.username);
  form.append('password', values.password);
  return axios.post(routes.signupPath, form);
};

const postMeme = async (form, accessToken) => axios.post(routes.memesPath, form, {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});

const validateToken = async (accessToken) => {
  if (!accessToken) {
    return false;
  }
  try {
    const response = await axios.get(`${routes.validateTokenPath}/${accessToken}`);
    return response.status === 200;
  } catch (e) {
    console.log('validate error', e);
    return false;
  }
};

const getUser = async (userId, accessToken) => {
  const response = await axios.get(`${routes.usersPath}/${userId}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  return response.data;
};

export {
  getMessages,
  loginUser,
  postMeme,
  signupUser,
  validateToken,
  getUser,
};
