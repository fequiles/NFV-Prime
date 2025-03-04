"use client";

import "./style.css";
import { Button, Form, FormInstance, Radio, TreeSelect, Upload } from "antd";
import FormTraffic from "./form";
import { useCallback, useEffect, useRef, useState } from "react";
import Card from "@/components/card";
import { notifyError } from "@/components/notification";
import InterfaceTraffic from "./list";
import { TrafficService } from "@/service/traffic";
import { IListTraffic, ITraffic } from "@/service/traffic/interface";
import { IListInterface } from "@/service/interfaces/interface";
import LoadingPage from "@/components/loading";
import { NFVPrimeService } from "@/service/nfvprime";
import { UploadOutlined } from "@ant-design/icons";
import { IExportedJson } from "@/service/nfvprime/interface";

interface IProps {
  interfacesList: IListInterface[];
  listTraffic: any[];
  setListTraffic: (list: any[]) => void;
  submitting: boolean;
  setSubmitting: (bool: boolean) => void;
  started: boolean;
  exportedJson: IExportedJson;
  setExportedJson: (obj: IExportedJson) => void;
}

export default function TrafficGenerator({
  interfacesList,
  listTraffic,
  setListTraffic,
  submitting,
  setSubmitting,
  started,
  exportedJson,
  setExportedJson
}: IProps) {
  const [loading, setLoading] = useState(true);
  const [treeValue, setTreeValue] = useState<string>();
  const [treeData, setTreeData] = useState<any[]>();
  const [form] = Form.useForm();
  const lineCounterRef = useRef<HTMLTextAreaElement>(null);
  const manualTrafficGeneratorRef = useRef<HTMLTextAreaElement>(null);
  const lineCountCache = useRef<number>(0);
  const [type, setType] = useState<string>("Automatic");
  const [manualTrafficGenerator, setManualTrafficGenerator] =
    useState<string>();

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        // call service
        const res = (await TrafficService.search()) as IListTraffic[];
        setTreeData(res);
      } catch (err: any) {
        notifyError({ content: err.message });
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  const syncTextAreas = useCallback(() => {
    if (manualTrafficGeneratorRef.current) {
      manualTrafficGeneratorRef.current.addEventListener("scroll", () => {
        if (lineCounterRef.current && manualTrafficGeneratorRef.current) {
          lineCounterRef.current.scrollTop =
            manualTrafficGeneratorRef.current.scrollTop;
          lineCounterRef.current.scrollLeft =
            manualTrafficGeneratorRef.current.scrollLeft;
        }
      });
    }
  }, []);

  const changeLineCounter = useCallback(() => {
    if (manualTrafficGeneratorRef.current && lineCounterRef.current) {
      let lineCount =
        manualTrafficGeneratorRef.current.value.split("\n").length;
      let outarr = new Array();
      if (lineCountCache.current != lineCount) {
        for (var x = 0; x < lineCount; x++) {
          outarr[x] = x + 1 + ".";
        }
        lineCounterRef.current.value = outarr.join("\n");
      }
      lineCountCache.current = lineCount;
    }
  }, []);

  const addLineCounter = useCallback(() => {
    if (manualTrafficGeneratorRef.current) {
      manualTrafficGeneratorRef.current.addEventListener("input", () => {
        changeLineCounter();
      });
    }
  }, []);

  const addTabHandler = useCallback(() => {
    if (manualTrafficGeneratorRef.current) {
      manualTrafficGeneratorRef.current.addEventListener(
        "keydown",
        (e: any) => {
          let { keyCode } = e;
          let { value, selectionStart, selectionEnd }: any =
            manualTrafficGeneratorRef.current;
          if (keyCode === 9 && manualTrafficGeneratorRef.current) {
            // TAB = 9
            e.preventDefault();
            manualTrafficGeneratorRef.current.value =
              value.slice(0, selectionStart) + "\t" + value.slice(selectionEnd);
            manualTrafficGeneratorRef.current.setSelectionRange(
              selectionStart + 1,
              selectionStart + 1
            );
          }
        }
      );
    }
  }, []);

  const removeTabHandler = useCallback(() => {
    if (manualTrafficGeneratorRef.current) {
      manualTrafficGeneratorRef.current.addEventListener(
        "keydown",
        (e: any) => {
          let { keyCode } = e;
          let { value, selectionStart, selectionEnd }: any =
            manualTrafficGeneratorRef.current;
          if (keyCode === 9 && manualTrafficGeneratorRef.current) {
            // TAB = 9
            e.preventDefault();
            manualTrafficGeneratorRef.current.value =
              value.slice(0, selectionStart) + "\t" + value.slice(selectionEnd);
            manualTrafficGeneratorRef.current.setSelectionRange(
              selectionStart + 1,
              selectionStart + 1
            );
          }
        }
      );
    }
  }, []);

  const findTextAreas = useCallback(() => {
    syncTextAreas();
    addLineCounter();
    addTabHandler();
  }, []);

  useEffect(() => {
    findTextAreas();

    return () => {
      removeTabHandler();
    };
  }, [findTextAreas]);

  const manualTrafficGeneratorChange = (e: any) => {
    const { value } = e.target;
    setManualTrafficGenerator(value);
  };

  if (loading) {
    return <LoadingPage />;
  }

  async function onSubmit() {
    setSubmitting(true);

    try {
      // call service
      if (type == "Automatic") {
        const values = await form.validateFields();
        values["type"] = type;
        let newList = [...listTraffic, values];
        setListTraffic(newList);
        let newExported = {...exportedJson}
        newExported.traffics = newList
        setExportedJson(newExported)
      } else {
        const values = {
          type: "Personal",
          name: "Manual Traffic Generator",
          code: manualTrafficGenerator,
        };
        let newList = [...listTraffic, values];
        setListTraffic(newList);
        let newExported = {...exportedJson}
        newExported.traffics = newList
        setExportedJson(newExported)
      }
    } catch (err: any) {
      notifyError({ content: err?.message });
    } finally {
      setSubmitting(false);
    }
  }

  const onChangeTree = (newValue: string) => {
    setTreeValue(newValue);
    const values = newValue.split(",");
    form.setFieldsValue({
      name: values[0],
      rate: parseInt(values[1]),
      lenght: parseInt(values[2]),
      count: parseInt(values[3]),
      delay: parseInt(values[4]),
      port: parseInt(values[5]),
      trigger: parseInt(values[6]),
    });
  };

  const onChangeRadio = (event) => {
    setType(event.target.value);
  };

  const handleChange = (info) => {
    // Prevent automatic upload
    if (info.file.status !== "uploading") {
      const file = info.file.originFileObj;
      if (file) {
        const reader = new FileReader();
        reader.readAsText(file);
        reader.onload = () => {
          const text = String(reader.result);
          setManualTrafficGenerator(text);
        };
      }
    }
  };

  return (
    <div className="container-traffic">
      <div className="card-traffic">
        <Card>
          <span>Traffic Configuration</span>
          <br />
          <div className="actions-traffic">
            <Radio.Group
              value={type}
              defaultValue="Automatic"
              buttonStyle="solid"
              onChange={onChangeRadio}
              style={{
                marginBottom: "10px",
                marginTop: "10px",
              }}
            >
              <Radio.Button value="Automatic">Automatic</Radio.Button>
              <Radio.Button value="Personal">Manual</Radio.Button>
            </Radio.Group>

            {type === "Personal" && (
              <Upload
                showUploadList={false}
                accept=".py, .txt"
                onChange={handleChange}
              >
                <Button icon={<UploadOutlined />}>Upload</Button>
              </Upload>
            )}
          </div>

          {type == "Automatic" ? (
            <>
              <TreeSelect
                style={{ width: "100%", marginBottom: "10px" }}
                value={treeValue}
                dropdownStyle={{
                  maxHeight: 400,
                  overflow: "auto",
                  margin: "1px",
                }}
                treeData={treeData}
                placeholder="Pre Configured Traffic Profiles (Optional)"
                treeDefaultExpandAll
                onChange={onChangeTree}
              />
              <FormTraffic
                form={form}
                submitting={submitting}
                interfaceList={interfacesList}
              />
            </>
          ) : (
            <>
              <textarea
                id="lineCounter"
                ref={lineCounterRef}
                wrap="off"
                disabled
              >
                1.
              </textarea>
              <textarea
                value={manualTrafficGenerator}
                id="codeEditor"
                ref={manualTrafficGeneratorRef}
                wrap="off"
                onChange={manualTrafficGeneratorChange}
              ></textarea>
            </>
          )}
          <div className="actions">
            <Button
              type="default"
              id="btn-start"
              onClick={onSubmit}
              disabled={started}
            >
              Add to List of Traffic to Generate
            </Button>
          </div>
        </Card>

        <Card>
          <InterfaceTraffic
            listTraffic={listTraffic}
            setListTraffic={setListTraffic}
            form={form}
            setType={setType}
            setManualTrafficGenerator={setManualTrafficGenerator}
            exportedJson={exportedJson}
            setExportedJson={setExportedJson}
          />
        </Card>
      </div>
    </div>
  );
}
