"use client";

import { NFVPrimeService } from "@/service/nfvprime";
import { FormInstance } from "antd";
import { Chart, registerables } from "chart.js/auto";
import { useEffect, useRef, useState } from "react";

Chart.register(...registerables);

interface IProps {
  form: FormInstance;
  interfaceMode: boolean;
}

export default function Canvas({ form, interfaceMode }: IProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const chartRef = useRef<Chart | null>(null);
  const labelRef = useRef(0);
  const [dadosRx, setDadosRx] = useState<number[]>([0]);
  const [dadosTx, setDadosTx] = useState<number[]>([0]);
  const [label, setLabel] = useState<number[]>([0]);

  const canvasProgramRef = useRef<HTMLCanvasElement>(null);
  const chartProgramRef = useRef<Chart | null>(null);
  const labelProgramRef = useRef(0);
  const lastDummy = useRef(null);
  const [dadosMem, setDadosMem] = useState<number[]>([0]);
  const [dadosCpu, setDadosCpu] = useState<number[]>([0]);
  const [labelProgram, setLabelProgram] = useState<number[]>([0]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");

    const nextLabel = label.toReversed().at(0);
    labelRef.current = nextLabel !== undefined ? nextLabel + 1 : 0;

    if (!canvas || !ctx) {
      return;
    }

    if (chartRef.current) {
      chartRef.current.data.labels = label;
      chartRef.current.data.datasets[0].data = dadosRx;
      chartRef.current.data.datasets[1].data = dadosTx;
      chartRef.current.update();
      return;
    }

    chartProgramRef.current?.destroy();
    chartProgramRef.current = null;
    chartRef.current = new Chart(ctx, {
      type: "line",
      data: {
        labels: label,
        datasets: [
          {
            label: "RX Bytes",
            data: dadosRx,
            backgroundColor: "#66791b",
            borderColor: "#66791b",
          },
          {
            label: "TX Bytes",
            data: dadosTx,
            backgroundColor: "#4096ff",
            borderColor: "#4096ff",
          },
        ],
      },
      options: {
        scales: {
          x: {
            title: {
              display: true,
              text: "seconds",
            },
          },
          y: {
            title: {
              display: true,
              text: "bytes",
            },
          },
        },
        interaction: {
          mode: "index",
          intersect: false,
        },
        animation: {
          duration: 0,
        },
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "RX & TX",
          },
        },
      },
    });
  }, [dadosRx, dadosTx, label]);

  const checkArrayLenghtToAdd = (
    array: number[],
    addValue: number,
    changedDummy: boolean
  ) => {
    if (changedDummy) {
      array = [];
    } else if (array.length > 60) {
      array.shift();
    }
    return [...array, addValue];
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      const values = await form.validateFields();
      let changedDummy = false;
      if (lastDummy.current != values["interface"]) {
        changedDummy = true;
        lastDummy.current = values["interface"];
      }

      let res1 = 0,
        res2 = 0;
      const res = await NFVPrimeService.getTrafficInfos();
      if (res != "Arquivo não encontrado!") {
        let dadosResult = res;
        let interfaceId = values["interface"];
        if (dadosResult[interfaceId]) {
          res1 = dadosResult[interfaceId]["rx"];
          res2 = dadosResult[interfaceId]["tx"];
        }
      }

      setDadosRx((e): number[] => checkArrayLenghtToAdd(e, res1, changedDummy));
      setDadosTx((e): number[] => checkArrayLenghtToAdd(e, res2, changedDummy));
      setLabel((e): number[] =>
        checkArrayLenghtToAdd(e, labelRef.current, changedDummy)
      );
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  useEffect(() => {
    const canvas = canvasProgramRef.current;
    const ctx = canvas?.getContext("2d");

    const nextLabel = labelProgram.toReversed().at(0);
    labelProgramRef.current = nextLabel !== undefined ? nextLabel + 1 : 0;

    if (!canvas || !ctx) {
      return;
    }

    if (chartProgramRef.current) {
      chartProgramRef.current.data.labels = labelProgram;
      chartProgramRef.current.data.datasets[0].data = dadosMem;
      chartProgramRef.current.data.datasets[1].data = dadosCpu;
      chartProgramRef.current.update();
      return;
    }

    chartRef.current?.destroy();
    chartRef.current = null;
    chartProgramRef.current = new Chart(ctx, {
      type: "line",
      data: {
        labels: labelProgram,
        datasets: [
          {
            label: "Mem %",
            data: dadosMem,
            backgroundColor: "#66791b",
            borderColor: "#66791b",
          },
          {
            label: "Cpu %",
            data: dadosCpu,
            backgroundColor: "#4096ff",
            borderColor: "#4096ff",
          },
        ],
      },
      options: {
        interaction: {
          mode: "index",
          intersect: false,
        },
        animation: {
          duration: 0,
        },
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "MEM & CPU",
          },
        },
      },
    });
  }, [dadosMem, dadosCpu, labelProgram]);

  useEffect(() => {
    const interval = setInterval(async () => {
      let res1 = 0,
        res2 = 0;
      const res = await NFVPrimeService.getProcessInfos();
      if (res != "Arquivo não encontrado!") {
        let dadosResult = res;
        let processName = "program";
        if (dadosResult && dadosResult[processName]) {
          res1 = dadosResult[processName]["mem"];
          res2 = dadosResult[processName]["cpu"];
        }
      }

      setDadosMem((e): number[] => checkArrayLenghtToAdd(e, res1, false));
      setDadosCpu((e): number[] => checkArrayLenghtToAdd(e, res2, false));
      setLabelProgram((e): number[] =>
        checkArrayLenghtToAdd(e, labelProgramRef.current, false)
      );
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <>
      {interfaceMode ? (
        <canvas ref={canvasRef} height="75"></canvas>
      ) : (
        <canvas ref={canvasProgramRef} height="75"></canvas>
      )}
    </>
  );
}
