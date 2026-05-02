import{w as h,u as p,e as d}from"./index-L_HRuGby.js";import{j as t}from"./jsx-runtime-D_zvdyIk.js";import{r as y}from"./index-CXOcBcs0.js";import{c as l}from"./utils-BQHNewu7.js";import"./_commonjsHelpers-CqkleIqs.js";function u({entries:n=[],className:r,maxHeight:c="400px"}){const[s,x]=y.useState("all"),m=s==="all"?n:n.filter(e=>e.source===s);return t.jsxs("div",{className:l("rounded-lg border bg-card p-4",r),children:[t.jsxs("div",{className:"mb-3 flex items-center justify-between",children:[t.jsx("h3",{className:"font-semibold text-card-foreground text-sm",children:"Transcript"}),t.jsx("div",{className:"flex gap-1",children:["all","microphone","system"].map(e=>t.jsx("button",{type:"button",onClick:()=>x(e),className:l("rounded-md px-2 py-1 text-xs capitalize transition-colors",s===e?"bg-primary text-primary-foreground":"bg-muted text-muted-foreground hover:bg-accent"),children:e},e))})]}),t.jsx("div",{className:"space-y-2 overflow-y-auto",style:{maxHeight:c},role:"log","aria-live":"polite",children:m.length===0?t.jsx("p",{className:"text-muted-foreground text-sm",children:"No transcript entries yet."}):m.map(e=>t.jsxs("div",{className:l("rounded-md p-2 text-sm",e.source==="microphone"?"bg-blue-50 dark:bg-blue-950":"bg-gray-50 dark:bg-gray-900"),children:[t.jsx("span",{className:"font-medium text-muted-foreground text-xs uppercase",children:e.source}),t.jsx("p",{className:"mt-0.5",children:e.text})]},e.id))})]})}u.__docgenInfo={description:"",methods:[],displayName:"TranscriptViewer",props:{entries:{required:!1,tsType:{name:"Array",elements:[{name:"TranscriptEntry"}],raw:"TranscriptEntry[]"},description:"",defaultValue:{value:"[]",computed:!1}},className:{required:!1,tsType:{name:"string"},description:""},maxHeight:{required:!1,tsType:{name:"string"},description:"",defaultValue:{value:'"400px"',computed:!1}}}};const g=[{id:"1",text:"Hej, jeg vil gerne høre om mine pensionsordninger.",source:"microphone",timestamp:"2026-04-29T10:00:00Z"},{id:"2",text:"Selvfølgelig! Lad mig hente dine oplysninger.",source:"system",timestamp:"2026-04-29T10:00:02Z"},{id:"3",text:"Jeg har tre aktive ordninger hos AP Pension.",source:"system",timestamp:"2026-04-29T10:00:05Z"},{id:"4",text:"Kan du fortælle mig mere om den største?",source:"microphone",timestamp:"2026-04-29T10:00:08Z"}],b={title:"Components/TranscriptViewer",component:u,parameters:{layout:"padded"},tags:["autodocs"]},a={args:{entries:[]}},i={args:{entries:g}},o={args:{entries:g},play:async({canvasElement:n})=>{const r=h(n);await p.click(r.getByText("microphone"));const c=r.getAllByText(/pensionsordninger|fortælle/);await d(c.length).toBe(2),await p.click(r.getByText("all"));const s=r.getAllByText(/microphone|system/i);await d(s.length).toBeGreaterThanOrEqual(4)}};a.parameters={...a.parameters,docs:{...a.parameters?.docs,source:{originalSource:`{
  args: {
    entries: []
  }
}`,...a.parameters?.docs?.source}}};i.parameters={...i.parameters,docs:{...i.parameters?.docs,source:{originalSource:`{
  args: {
    entries: sampleEntries
  }
}`,...i.parameters?.docs?.source}}};o.parameters={...o.parameters,docs:{...o.parameters?.docs,source:{originalSource:`{
  args: {
    entries: sampleEntries
  },
  play: async ({
    canvasElement
  }) => {
    const canvas = within(canvasElement);

    // Click "microphone" filter
    await userEvent.click(canvas.getByText("microphone"));

    // Should only show microphone entries
    const entries = canvas.getAllByText(/pensionsordninger|fortælle/);
    await expect(entries.length).toBe(2);

    // Click "all" to reset
    await userEvent.click(canvas.getByText("all"));
    const allEntries = canvas.getAllByText(/microphone|system/i);
    await expect(allEntries.length).toBeGreaterThanOrEqual(4);
  }
}`,...o.parameters?.docs?.source}}};const j=["Empty","WithEntries","FilterInteraction"];export{a as Empty,o as FilterInteraction,i as WithEntries,j as __namedExportsOrder,b as default};
