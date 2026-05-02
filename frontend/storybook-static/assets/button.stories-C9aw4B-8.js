import{w as O,u as j,e as z,f as E}from"./index-L_HRuGby.js";import{j as D}from"./jsx-runtime-D_zvdyIk.js";import{a as _,c as T}from"./utils-BQHNewu7.js";import{r as G}from"./index-CXOcBcs0.js";import"./_commonjsHelpers-CqkleIqs.js";const C=r=>typeof r=="boolean"?`${r}`:r===0?"0":r,w=_,R=(r,a)=>e=>{var o;if(a?.variants==null)return w(r,e?.class,e?.className);const{variants:l,defaultVariants:i}=a,B=Object.keys(l).map(n=>{const t=e?.[n],c=i?.[n];if(t===null)return null;const s=C(t)||C(c);return l[n][s]}),x=e&&Object.entries(e).reduce((n,t)=>{let[c,s]=t;return s===void 0||(n[c]=s),n},{}),V=a==null||(o=a.compoundVariants)===null||o===void 0?void 0:o.reduce((n,t)=>{let{class:c,className:s,...L}=t;return Object.entries(L).every(N=>{let[S,b]=N;return Array.isArray(b)?b.includes({...i,...x}[S]):{...i,...x}[S]===b})?[...n,c,s]:n},[]);return w(r,B,V,e?.class,e?.className)},A=R("inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",{variants:{variant:{default:"bg-primary text-primary-foreground hover:bg-primary/90",destructive:"bg-destructive text-destructive-foreground hover:bg-destructive/90",outline:"border border-input bg-background hover:bg-accent hover:text-accent-foreground",secondary:"bg-secondary text-secondary-foreground hover:bg-secondary/80",ghost:"hover:bg-accent hover:text-accent-foreground",link:"text-primary underline-offset-4 hover:underline"},size:{default:"h-10 px-4 py-2",sm:"h-9 rounded-md px-3",lg:"h-11 rounded-md px-8",icon:"h-10 w-10"}},defaultVariants:{variant:"default",size:"default"}}),k=G.forwardRef(({className:r,variant:a,size:e,...o},l)=>D.jsx("button",{className:T(A({variant:a,size:e,className:r})),ref:l,...o}));k.displayName="Button";k.__docgenInfo={description:"",methods:[],displayName:"Button",composes:["ButtonHTMLAttributes","VariantProps"]};const K={title:"UI/Button",component:k,parameters:{layout:"centered"},tags:["autodocs"],argTypes:{variant:{control:{type:"select"},options:["default","destructive","outline","secondary","ghost","link"]},size:{control:{type:"select"},options:["default","sm","lg","icon"]}},args:{onClick:E()}},d={args:{children:"Button"}},u={args:{variant:"destructive",children:"Delete"}},m={args:{variant:"outline",children:"Outline"}},v={args:{variant:"secondary",children:"Secondary"}},g={args:{variant:"ghost",children:"Ghost"}},p={args:{variant:"link",children:"Link"}},h={args:{size:"sm",children:"Small"}},y={args:{size:"lg",children:"Large"}},f={args:{children:"Click me"},play:async({canvasElement:r,args:a})=>{const e=O(r);await j.click(e.getByRole("button")),await z(a.onClick).toHaveBeenCalledTimes(1)}};d.parameters={...d.parameters,docs:{...d.parameters?.docs,source:{originalSource:`{
  args: {
    children: "Button"
  }
}`,...d.parameters?.docs?.source}}};u.parameters={...u.parameters,docs:{...u.parameters?.docs,source:{originalSource:`{
  args: {
    variant: "destructive",
    children: "Delete"
  }
}`,...u.parameters?.docs?.source}}};m.parameters={...m.parameters,docs:{...m.parameters?.docs,source:{originalSource:`{
  args: {
    variant: "outline",
    children: "Outline"
  }
}`,...m.parameters?.docs?.source}}};v.parameters={...v.parameters,docs:{...v.parameters?.docs,source:{originalSource:`{
  args: {
    variant: "secondary",
    children: "Secondary"
  }
}`,...v.parameters?.docs?.source}}};g.parameters={...g.parameters,docs:{...g.parameters?.docs,source:{originalSource:`{
  args: {
    variant: "ghost",
    children: "Ghost"
  }
}`,...g.parameters?.docs?.source}}};p.parameters={...p.parameters,docs:{...p.parameters?.docs,source:{originalSource:`{
  args: {
    variant: "link",
    children: "Link"
  }
}`,...p.parameters?.docs?.source}}};h.parameters={...h.parameters,docs:{...h.parameters?.docs,source:{originalSource:`{
  args: {
    size: "sm",
    children: "Small"
  }
}`,...h.parameters?.docs?.source}}};y.parameters={...y.parameters,docs:{...y.parameters?.docs,source:{originalSource:`{
  args: {
    size: "lg",
    children: "Large"
  }
}`,...y.parameters?.docs?.source}}};f.parameters={...f.parameters,docs:{...f.parameters?.docs,source:{originalSource:`{
  args: {
    children: "Click me"
  },
  play: async ({
    canvasElement,
    args
  }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole("button"));
    await expect(args.onClick).toHaveBeenCalledTimes(1);
  }
}`,...f.parameters?.docs?.source}}};const M=["Default","Destructive","Outline","Secondary","Ghost","Link","Small","Large","WithClick"];export{d as Default,u as Destructive,g as Ghost,y as Large,p as Link,m as Outline,v as Secondary,h as Small,f as WithClick,M as __namedExportsOrder,K as default};
