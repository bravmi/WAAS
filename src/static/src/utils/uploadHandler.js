import removeFileExtension from "./removeFileExtension.js";

const uploadHandler = async ({
  file,
  setErrorMessage,
  setUploadStatus,
  setJobId,
  selectedLanguage,
  selectedModel,
  email,
}) => {
  try {
    const apiUrl = new URL(`${window.location.href}v1/transcribe`);
    const urlFormattedEmail = encodeURIComponent(email);
    const urlFormattedFileName = encodeURIComponent(removeFileExtension(file.name));

    apiUrl.searchParams.set("model", selectedModel || "base");
    apiUrl.searchParams.set("email_callback", urlFormattedEmail || "");

    if (file.name){
      apiUrl.searchParams.set("filename", urlFormattedFileName);
    }

    if (selectedLanguage !== "detect-language" && selectedLanguage) {
      apiUrl.searchParams.set("language", selectedLanguage);
    }

    setUploadStatus("uploading");

    const fileReader = new FileReader();
    fileReader.readAsArrayBuffer(file);

    const arrayBuffer = await new Promise((resolve, reject) => {
      fileReader.onload = (event) => resolve(event.target.result);
      fileReader.onerror = (error) => reject(error);
    });

    const response = await fetch(apiUrl.toString(), {
      method: "POST",
      headers: {
        "Content-Type": file.type,
      },
      body: arrayBuffer,
    });

    if (!response.ok) {
      return setErrorMessage("Something went wrong");
    }

    const data = await response.json();

    setUploadStatus("queued");
    setJobId(data.job_id);
  } catch (error) {
    setErrorMessage(error.message);
  }
};

export default uploadHandler;
