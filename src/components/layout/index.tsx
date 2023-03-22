import { FC, PropsWithChildren } from "react";
import { IMeta } from "../seo/IMeta";
import Meta from "../seo/Meta";
import Header from "./Header";
import Footer from "./Footer";

const Layout: FC<PropsWithChildren<IMeta>> = ({
  title,
  description,
  children,
}) => {
  return (
    <Meta title={title} description={description}>
      <Header />
      {children}
      <Footer />
    </Meta>
  );
};

export default Layout;
