import Layout from "@/components/layout";
import { PostsService } from "@/services/posts-service";
import { GetServerSideProps, NextPage } from "next";
import { FC } from "react";

const HomePage: FC = ({ posts }) => {
  console.log(posts);
  return (
    <Layout title="Home" description="Home page">
      <h1>Welcome</h1>
    </Layout>
  );
};

export default HomePage;
