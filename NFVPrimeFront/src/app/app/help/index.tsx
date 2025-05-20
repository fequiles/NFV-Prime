"use client";

import "./style.css";

export default function Help() {

  return (
    <div>
      Welcome to NFV-Prime! Follow the next steps to use our platform. Enjoy! <br /><br />
      <b>1.</b> Use our VNF Code Editor to write/upload your function or select a function provided by us.  <br />
      <b>2.</b> Use our Virtal Network Interfaces Manager to create virtual network interfaces. You can use 2 virtual network interfaces that have already been created: dummy2_1 & dummy2_2. <br />
      <b>3.</b> Use our Traffic Generator to configure the traffics be sent to the interfaces after your VNF is instantiated. There are several predefined traffic profiles that you can use. <br />
      <b>4.</b> Use the Visualization module to select the virtual interface and/or function that you want to monitor visually.<br />
      <b>5.</b> Press the Start button to initialize all processes. You can stop all processes pressing Stop button.<br />
    </div>
  );
}
