
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { FormikProvider, useFormik } from "formik";
import Form from 'react-bootstrap/Form';
import React, { useEffect, useState } from "react";
import { getUserIdFromStorage } from '../utils/utils';
import { getMessages, getUsers } from '../utils/requests';


const ws = new WebSocket(`ws://127.0.0.1:8000/chat/ws`);


const IndexPage = ({ show, onHide }) => {
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState([]);
  const access_token = localStorage.getItem('user')

  const currentUserId = getUserIdFromStorage();

//   get all messages
  useEffect(() => {
    getMessages(access_token)
      .then((messages) => {
        setMessages(messages)
      });
  }, [])

  //   get all users
  useEffect(() => {
    getUsers(access_token)
      .then((users) => {
        setUsers(users)
      });
  }, [])

  console.log('users', users)
  console.log('messages', messages)
  ws.onmessage = (event) => {
    const receivedJson = JSON.parse(event.data)
    setMessages([...messages, receivedJson])
  };

  const handleMessageSubmit = async (event) => {
    try {
      const message = {
        author: currentUserId,
        receiver: Number(event.receiver),
        text: event.message,
      }
      ws.send(JSON.stringify(message))
    } catch (e) {
      console.log(e);
    }
  }

    const formik = useFormik({
        initialValues: {
            message: '',
            receiver: '',
        },
        onSubmit: (messageObject, { resetForm }) => {
          console.log('messageObject', messageObject)
          handleMessageSubmit(messageObject);
          resetForm();
        },
    });

  return (
    <>
      <div className='d-flex flex-column h-100 my-5'>
        <div className='container-fluid h-100'>
          <div className='row justify-content-center align-content-center h-100'>
            <div className='col-md-6'>
              <div className='card shadow-sm'>
                <div className='card-body row p-5'>

                  <FormikProvider value={formik}>
                    <Form onSubmit={formik.handleSubmit} noValidate="" className="py-1 border-0">
                      <Form.Label>Введите сообщение</Form.Label>
                      <Form.Group className="input-group has-validation">
                      <Form.Control
                        aria-label="Введите сообщение"
                        placeholder=""
                        autoComplete="message"
                        id="message"
                        name="message"
                        type="text"
                        className=" border border-dark border-2 rounded-4 p-0 ps-2"
                        onChange={formik.handleChange}
                        value={formik.values.message} />
                      </Form.Group>
                      <Form.Label>Выберите получателя</Form.Label>
                      <Form.Select
                        className="my-3"
                        id="receiver"
                        name="receiver"
                        onChange={formik.handleChange}>
                        {users.map((user) => {
                          const userId = user.id
                          return <option key={userId} value={userId}>{user.username}</option>
                        })}
                      </Form.Select>
                      <Button type="submit" variant='outline-secondary'>
                        Отправить
                      </Button>
                    </Form>
                  </FormikProvider>

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>            


      <div className='d-flex flex-column h-100'>
        <div className='container-fluid h-100'>
          <div className='row justify-content-center align-content-center h-100'>
            <div className='col-md-6'>
              <div className='card shadow-sm'>
                <div className='card-body row p-5'>
                  <h4>Полученные сообщения</h4>
                  {messages && messages.map((message) => {
                    if (message.receiver.id === currentUserId) {
                      const createdAt = message.created_at
                      const formatedDate= new Date(Date.parse(createdAt));
                  
                      const messageTime = `${formatedDate.getHours()}:${formatedDate.getMinutes()}`
                      const messageDate = `${formatedDate.toLocaleDateString("ru-RU")}`
                      const dateFormat = `${messageDate}: ${messageTime}`;
                      return <div key={message.id} className="text-break mb-2">
                              <strong className="fs-6">{message.author.username} </strong>
                              <em>{dateFormat}: </em>
                              <span>{message.text}</span>
                            </div>
                    }
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className='d-flex flex-column h-100'>
        <div className='container-fluid h-100'>
          <div className='row justify-content-center align-content-center h-100'>
            <div className='col-md-6'>
              <div className='card shadow-sm'>
                <div className='card-body row p-5'>
                  <h4>Отправленные сообщения</h4>
                  {messages && messages.map((message) => {
                    if (message.author.id === currentUserId) {
                      const createdAt = message.created_at
                      const formatedDate= new Date(Date.parse(createdAt));
                  
                      const messageTime = `${formatedDate.getHours()}:${formatedDate.getMinutes()}`
                      const messageDate = `${formatedDate.toLocaleDateString("ru-RU")}`
                      const dateFormat = `${messageDate}: ${messageTime}`;
                      return <div key={message.id} className="text-break mb-2">
                              <strong className="fs-6">{message.author.username} </strong>
                              <em>{dateFormat}: </em>
                              <span>{message.text}</span>
                            </div>
                    }
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default IndexPage;