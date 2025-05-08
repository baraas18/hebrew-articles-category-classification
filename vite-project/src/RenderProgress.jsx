import React from "react"
import { createTheme, styled } from "@mui/material"
import clsx from "clsx"

const defaultTheme = createTheme();

const ProgressBarRoot = styled("div")(({ theme }) => ({
  border: `1px solid ${theme.palette.divider}`,
  position: "relative",
  overflow: "hidden",
  width: "100%",
  height: 26,
  borderRadius: 2
}));

const ProgressBarValue = styled("div")({
  position: "absolute",
  lineHeight: "24px",
  width: "100%",
  justifyContent: "center",
  display: 'flex'
});

const ProgressBarBar = styled("div")(({ theme }) => ({
  height: "100%",
  "&.low": {
    backgroundColor: "#f44336",
  },
  "&.medium": {
    backgroundColor: "#efbb5aa3",
  },
  "&.high": {
    backgroundColor: "#088208a3",
  },
}));

const ProgressBar = React.memo(function ProgressBar(props) {
  const { value } = props;
  const valueInPercent = value * 100;

  return (
    <ProgressBarRoot>
          <ProgressBarValue>{`${valueInPercent.toLocaleString()} %`}</ProgressBarValue>
      <ProgressBarBar
        className={clsx({
          low: valueInPercent < 30,
          medium: valueInPercent >= 30 && valueInPercent <= 70,
          high: valueInPercent > 70,
        })}
        style={{ maxWidth: `${valueInPercent}%` }}
      />
    </ProgressBarRoot>
  );
});

export function renderProgress(params) {
  return <ProgressBar value={params.value} />;
}