import OpenCC from 'opencc-js';
const convert=OpenCC.Converter({from:'cn',to:'tw'});
export function traditional(value){
 if(typeof value==='string')return convert(value).replaceAll('文件夾','資料夾').replaceAll('文件','檔案').replaceAll('內核','核心').replaceAll('服務器','伺服器').replaceAll('賬號','帳號').replaceAll('軟件','軟體');
 if(Array.isArray(value))return value.map(traditional);
 if(value&&typeof value==='object')return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,traditional(v)]));
 return value;
}
