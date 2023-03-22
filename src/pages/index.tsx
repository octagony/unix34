import HomePage from "@/components/screens/Home";
import { PostsService } from "@/services/posts-service";
import { GetServerSideProps } from "next";
import { Ubuntu } from "next/font/google";

const ubuntu = Ubuntu({
  subsets: ["latin"],
  weight: ["300", "400", "500", "700"],
});

const Home: NextPage = ({ posts }) => {
  return (
    <div className={ubuntu.className}>
      <HomePage posts={posts} />
    </div>
  );
};

export const getServerSideProps: GetServerSideProps = async () => {
  const { data: posts } = await PostsService.getHot();
  return {
    props: {
      posts: posts.resp,
    },
  };
};

export default Home;
