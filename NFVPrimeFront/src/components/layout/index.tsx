"use client";

import "./style.css";
import React, { ReactNode, useCallback, useEffect, useRef, useState } from "react";
import {
  HomeOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from "@ant-design/icons";
import { Layout, Menu, Button, Flex } from "antd";
import { AuthService } from "@/service/auth";
import LoadingPage from "../loading";

const { Header, Sider, Content, Footer } = Layout;

interface IProps {
  children: ReactNode;
}

export default function LayoutPage({ children }: IProps) {
  const [collapsed, setCollapsed] = useState(false);
  const name = useRef<string | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(true);



  useEffect(() => {
      name.current = AuthService.Username
      setLoading(false)
  }, []);

  function onSignOut() {
    AuthService.signOut();
    window.location.reload();
  }

  if (!name.current) {
    return <div className="div-login">{children}</div>;
  }

  if (loading) {
    return <LoadingPage/>
  }

  return (
      <Layout style={{ minHeight: '100vh' }}>
        <Sider
          trigger={null}
          collapsible
          collapsed={collapsed}
          className="navbar"
        >
          <div className="demo-logo-vertical" />
          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            items={[
              {
                key: "1",
                icon: <HomeOutlined />,
                label: "Home",
              },
              {
                key: "99",
                icon: <LogoutOutlined />,
                label: "Exit",
                onClick: onSignOut,
              },
            ]}
          />
        </Sider>
        <Layout style={{
          marginBottom:'60px',
          overflow: 'auto'
        }}>
          <Header>
            <div>
              <Button
                type="text"
                icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
                onClick={() => setCollapsed(!collapsed)}
                className="btn-collapse"
              />

              <span className="header-name">{`Welcome, ${
                name.current ?? "- "
              }!`}</span>
            </div>
          </Header>
          <Content className="layout-content">{children}</Content>
        </Layout>
        <Footer style={{ 
          borderTop: '1px solid #e8e8e8',
          justifyContent: 'center',
          position: 'fixed',
          left: 0,
          bottom: 0,
          width: '100%',
          backgroundColor: 'white',
          textAlign: 'center',
        }}>
          NFV-Prime © {new Date().getFullYear()} Created by Felipe Quiles 
        </Footer>
      </Layout>
  );
}
