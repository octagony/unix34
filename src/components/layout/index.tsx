import { FC, PropsWithChildren } from "react";
import { IMeta } from "../seo/IMeta";

const Layout: FC<PropsWithChildren<IMeta>> = ({
  title,
  description,
  children,
}) => {
  return <p>Layout</p>;
};

export default Layout;
