"use client";

import "./style.css";

export default function Help() {

  return (
    <div>
      Welcome to NFV-Prime! Follow the next steps to use our platform. Enjoy! <br /><br />
      <b>1.</b> On VNF Code Editor, write/upload your function or select a function provided by us.  <br />
      <b>2.</b> On Virtal Network Interfaces Manager, create virtual network interfaces. We already create 2 of them. And we have a traffic generator interface too. <br />
      <b>3.</b> On Traffic Generator, configure the traffics who is been sent to the interfaces when we instantiate your VNF. We have some options of literature traffic profiles for you. <br />
      <b>4.</b> On Visualization, select the virtual interface or process that you want to see graphics statistics.<br />
      <b>5.</b> Press the Start button to initialize all process. Analyze the results. You can stop all processes pressing Stop button.<br />
    </div>
  );
}
