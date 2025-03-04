import { Icon } from "./interface";

import {
  MdChecklist,
  MdEditNote,
  MdOutlineMailOutline,
  MdHistory,
  MdLanguage,
  MdLogout,
  MdPhone,
  MdOutlineSchool,
  MdOutlineDelete,
  MdInfo,
  MdClose,
  MdOutlineRemoveRedEye,
  MdOutlineRefresh,
  MdRadioButtonChecked,
  MdCheckCircle,
  MdRadioButtonUnchecked,
  MdHelp,
  MdKeyboardArrowDown,
  MdKeyboardArrowUp,
  MdOutlineFileUpload,
  MdUploadFile,
  MdOutlineFileDownload,
  MdOutlineShare,
  MdWhatsapp,
  MdOutlineLiveHelp,
  MdChat,
  MdOutlinePrint,
  MdOutlineSend,
  MdError,
} from "react-icons/md";

import {
  AiOutlineLoading,
  AiOutlineMinusCircle,
  AiOutlinePlus,
} from "react-icons/ai";

interface IProps {
  id: Icon;
}

function getIcon(id: Icon) {
  switch (id) {
    case Icon.Checklist:
      return <MdChecklist />;
    case Icon.EditNote:
      return <MdEditNote />;
    case Icon.Email:
      return <MdOutlineMailOutline />;
    case Icon.Hitory:
      return <MdHistory />;
    case Icon.Home:
      return <MdLanguage />;
    case Icon.Logout:
      return <MdLogout />;
    case Icon.Phone:
      return <MdPhone />;
    case Icon.Training:
      return <MdOutlineSchool />;
    case Icon.Delete:
      return <MdOutlineDelete />;
    case Icon.Info:
      return <MdInfo />;
    case Icon.Close:
      return <MdClose />;
    case Icon.Visible:
      return <MdOutlineRemoveRedEye />;
    case Icon.Refresh:
      return <MdOutlineRefresh />;
    case Icon.Radio:
      return <MdRadioButtonUnchecked />;
    case Icon.RadioCheck:
      return <MdRadioButtonChecked />;
    case Icon.Check:
      return <MdCheckCircle />;
    case Icon.Help:
      return <MdHelp />;
    case Icon.ArrowDown:
      return <MdKeyboardArrowDown />;
    case Icon.ArrowUp:
      return <MdKeyboardArrowUp />;
    case Icon.Upload:
      return <MdOutlineFileUpload />;
    case Icon.UploadFile:
      return <MdUploadFile />;
    case Icon.Loading:
      return <AiOutlineLoading />;
    case Icon.Add:
      return <AiOutlinePlus />;
    case Icon.RemoveCicle:
      return <AiOutlineMinusCircle />;
    case Icon.FileDownload:
      return <MdOutlineFileDownload />;
    case Icon.Share:
      return <MdOutlineShare />;
    case Icon.WhatsApp:
      return <MdWhatsapp />;
    case Icon.LiveHelp:
      return <MdOutlineLiveHelp />;
    case Icon.Chat:
      return <MdChat />;
    case Icon.Print:
      return <MdOutlinePrint />;
    case Icon.Send:
      return <MdOutlineSend />;
    case Icon.Error:
      return <MdError />;
    default:
      return <></>;
  }
}

export default function IconView({ id }: IProps) {
  return <i>{getIcon(id)}</i>;
}
