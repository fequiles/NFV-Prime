"use client";

import "./style.css";
import LoadingPage from "@/components/loading";
import { notifyError } from "@/components/notification";
import RedirectPage from "@/components/redirect";
import { AuthService } from "@/service/auth";
import { Button, Form, Input, Space } from "antd";
import { useEffect, useState } from "react";

interface ILogin {
  username: string;
  password: string;
}

export default function AuthLoginClient() {
  const [sending, setSending] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [redirect, setRedirect] = useState<string | undefined>(undefined);

  const [form] = Form.useForm();

  useEffect(() => {
    if (AuthService.Username) {
      setRedirect("/app");
    } else {
      AuthService.signOut();
    }

    setLoading(false);
  }, []);

  function onSubmit({ username }: ILogin) {
    setSubmitting(true);
    try {
      // call service
      AuthService.signIn(username);

      setSubmitted(true);
      // setRedirect("/app");
      window.location.reload();
    } catch (err: any) {
      console.log(err);
      notifyError({ content: err?.message });
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <LoadingPage />;
  }

  if (redirect) {
    return <RedirectPage url={redirect} />;
  }

  return (
    <Form
      onFinish={onSubmit}
      className="login-form-container"
      initialValues={{
        username: AuthService.Username ?? "",
        password: "",
      }}
      scrollToFirstError={{
        behavior: "smooth",
        block: "center",
        inline: "center",
      }}
      form={form}
      layout="vertical"
    >
      <Space direction="vertical" className="login-form" wrap>
        <Form.Item
          name="username"
          rules={[{ required: true, message: "Por favor, digite seu nome" }]}
          initialValue={AuthService.Username}
          label={"Nome"}
        >
          <Input
            type="text"
            disabled={submitting || sending}
            placeholder={"Digite o seu nome"}
            maxLength={150}
          />
        </Form.Item>

        <Button
          type="primary"
          htmlType="submit"
          loading={submitting || sending}
          className="login-buttom btn-icon"
        >
          Entrar
        </Button>
      </Space>
    </Form>
  );
}
