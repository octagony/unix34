import axios from "axios";
// const API_URL = "https://www.reddit.com/r/unixporn";
// axios.defaults.baseURL = API_URL;
export const PostsService = {
  async getHot() {
    const { data } = await axios.get(
      "https://www.reddit.com/r/unixporn/hot.json?limit=15"
    );
    return {
      data: {
        resp: data.data.children,
      },
    };
  },
};
