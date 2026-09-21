import fr from './translations/fr.json' with {type:'json'};
export const localizations={fr};
export function applyTopicLocalizations(topics){
 for(const [locale,data] of Object.entries(localizations))for(const topic of topics){
  const translated=data.topics[topic.id];if(!translated)continue;
  for(const key of ['title','goal','note','expected'])if(translated[key]){topic[key]??={};topic[key][locale]=translated[key];}
  for(const [i,step] of topic.steps.entries())for(const key of ['title','body','iphoneBody'])if(translated.steps?.[i]?.[key]){step[key]??={};step[key][locale]=translated.steps[i][key];}
 }
}
