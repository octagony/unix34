import * as React from "react";
import Box from "@mui/material/Box";
import BottomNavigation from "@mui/material/BottomNavigation";
import BottomNavigationAction from "@mui/material/BottomNavigationAction";
import WhatshotIcon from "@mui/icons-material/Whatshot";
import FiberNewIcon from "@mui/icons-material/FiberNew";
import StarIcon from "@mui/icons-material/Star";
import StackedLineChartIcon from "@mui/icons-material/StackedLineChart";
import { FC } from "react";

const Footer: FC = () => {
  const [value, setValue] = React.useState(0);

  return (
    <Box sx={{ width: 500 }}>
      <BottomNavigation
        showLabels
        value={value}
        onChange={(event, newValue) => {
          setValue(newValue);
        }}
      >
        <BottomNavigationAction label="Hot" icon={<WhatshotIcon />} />
        <BottomNavigationAction label="New" icon={<FiberNewIcon />} />
        <BottomNavigationAction label="Top" icon={<StarIcon />} />
        <BottomNavigationAction label="Rise" icon={<StackedLineChartIcon />} />
      </BottomNavigation>
    </Box>
  );
};
export default Footer;
