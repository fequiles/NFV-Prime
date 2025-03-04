"use client";

import "./style.css";
import { useCallback, useEffect, useRef, useState } from "react";
import Card from "@/components/card";
import { CodeEditorService } from "@/service/codeEditor";
import { notifyError, notifyInfo } from "@/components/notification";
import { Button, Divider, TreeSelect, Upload } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import { IExportedJson } from "@/service/nfvprime/interface";

interface IProps {
  code: string | undefined;
  setCode: (code: string) => void;
  exportedJson: IExportedJson;
  setExportedJson: (obj: IExportedJson) => void;
}

export default function CodeEditor({ code, setCode, exportedJson, setExportedJson }: IProps) {
  const lineCounterRef = useRef<HTMLTextAreaElement>(null);
  const codeEditorRef = useRef<HTMLTextAreaElement>(null);
  const lineCountCache = useRef<number>(0);
  const [playingCode, setPlayingCode] = useState(false);
  const [treeValue, setTreeValue] = useState<string>();
  const [treeData, setTreeData] = useState<any[]>();

  useEffect(() => {
    async function load() {
      try {
        // call service
        const res = await CodeEditorService.getSamples();
        setTreeData(res);
      } catch (err: any) {
        notifyError({ content: err.message });
      } finally {
      }
    }

    load();
  }, []);

  const syncTextAreas = useCallback(() => {
    if (codeEditorRef.current) {
      codeEditorRef.current.addEventListener("scroll", () => {
        if (lineCounterRef.current && codeEditorRef.current) {
          lineCounterRef.current.scrollTop = codeEditorRef.current.scrollTop;
          lineCounterRef.current.scrollLeft = codeEditorRef.current.scrollLeft;
        }
      });
    }
  }, []);

  const changeLineCounter = useCallback(() => {
    if (codeEditorRef.current && lineCounterRef.current) {
      let lineCount = codeEditorRef.current.value.split("\n").length;
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
    if (codeEditorRef.current) {
      codeEditorRef.current.addEventListener("input", () => {
        changeLineCounter();
      });
    }
  }, []);

  const addTabHandler = useCallback(() => {
    if (codeEditorRef.current) {
      codeEditorRef.current.addEventListener("keydown", (e: any) => {
        let { keyCode } = e;
        let { value, selectionStart, selectionEnd }: any =
          codeEditorRef.current;
        if (keyCode === 9 && codeEditorRef.current) {
          // TAB = 9
          e.preventDefault();
          codeEditorRef.current.value =
            value.slice(0, selectionStart) + "\t" + value.slice(selectionEnd);
          codeEditorRef.current.setSelectionRange(
            selectionStart + 1,
            selectionStart + 1
          );
        }
      });
    }
  }, []);

  const removeTabHandler = useCallback(() => {
    if (codeEditorRef.current) {
      codeEditorRef.current.addEventListener("keydown", (e: any) => {
        let { keyCode } = e;
        let { value, selectionStart, selectionEnd }: any =
          codeEditorRef.current;
        if (keyCode === 9 && codeEditorRef.current) {
          // TAB = 9
          e.preventDefault();
          codeEditorRef.current.value =
            value.slice(0, selectionStart) + "\t" + value.slice(selectionEnd);
          codeEditorRef.current.setSelectionRange(
            selectionStart + 1,
            selectionStart + 1
          );
        }
      });
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

  const programChange = (e: any) => {
    const { value } = e.target;
    setCode(value);
    let newExported = {...exportedJson}
    newExported.code = value
    setExportedJson(newExported)
  };

  const handlePlayingCode = () => {
    if (!playingCode) {
      if (code) {
        try {
          CodeEditorService.start(code);
          setPlayingCode(true);
        } catch (err: any) {
          notifyError({ content: err?.message });
        }
      } else {
        notifyInfo({ content: "O código do programa não pode estar vazio" });
      }
    } else {
      try {
        CodeEditorService.stop();
        setPlayingCode(false);
      } catch (err: any) {
        notifyError({ content: err?.message });
      }
    }
  };

  const onChangeTree = (newValue: string) => {
    setTreeValue(newValue);
    setCode(newValue);
    let newExported = {...exportedJson}
    newExported.code = newValue
    setExportedJson(newExported)
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
          setCode(text);
          let newExported = {...exportedJson}
          newExported.code = text
          setExportedJson(newExported)
        };
      }
    }
  };

  return (
    <div className="container-editor">
      <div className="title-editor">
        <div className="selector-editor">
          <TreeSelect
            style={{ width: "100%" }}
            value={treeValue}
            dropdownStyle={{ maxHeight: 400, overflow: "auto" }}
            treeData={treeData}
            placeholder="Select the Function (Optional)"
            treeDefaultExpandAll
            onChange={onChangeTree}
            className="tree-select"
          />
          <Upload
            showUploadList={false}
            accept=".py,.txt"
            onChange={handleChange}
          >
            <Button icon={<UploadOutlined />}>Upload</Button>
          </Upload>

          {/* {!playingCode
          ? <Button className="btn-icons float-right" shape="circle" icon={<PlayCircleOutlined />} onClick={handlePlayingCode} />
          : <Button className="btn-icons float-right" shape="circle" icon={<PauseCircleOutlined />} onClick={handlePlayingCode}/>} */}
        </div>
      </div>

      <Card className="code-editor">
        <textarea id="lineCounter" ref={lineCounterRef} wrap="off" disabled>
          1.
        </textarea>
        <textarea
          value={code}
          id="codeEditor"
          ref={codeEditorRef}
          wrap="off"
          onChange={programChange}
        ></textarea>
      </Card>
    </div>
  );
}
