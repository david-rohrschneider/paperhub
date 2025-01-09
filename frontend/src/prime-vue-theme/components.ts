export default {
  tag: {
    colorScheme: {
      light: {
        primaryBackground: "{primary.color}",
        primaryColor: "{primary.contrastColor}",
      },
      dark: {
        primaryBackground: "{primary.color}",
        primaryColor: "{primary.contrastColor}",
      },
    },
  },
  inputtext: {
    colorScheme: {
      light: {
        borderColor: "{zinc.400}",
        backgroundColor: "{zinc.50}",
        color: "{zinc.900}",
        placeholderColor: "{zinc.500}",
        focusColor: "{primary.color}",
        disabledColor: "{zinc.300}",
        disabledBackgroundColor: "{zinc.100}",
        errorColor: "{red.500}",
        errorBackgroundColor: "{red.100}",
      },
      dark: {
        borderColor: "{zinc.600}",
        backgroundColor: "{surface.800}",
        color: "{zinc.100}",
        placeholderColor: "{zinc.500}",
        focusColor: "{primary.color}",
        disabledColor: "{zinc.300}",
        disabledBackgroundColor: "{zinc.100}",
        errorColor: "{red.500}",
        errorBackgroundColor: "{red.100}",
      },
    },
  },
  progressspinner: {
    colorScheme: {
      light: {
        color: {
          1: "{primary.color}",
          2: "{primary.color}",
          3: "{primary.color}",
          4: "{primary.color}",
        },
      },
      dark: {
        color: {
          1: "{primary.color}",
          2: "{primary.color}",
          3: "{primary.color}",
          4: "{primary.color}",
        },
      },
    },
  },
  chip: {
    borderRadius: "0.25rem",
  },
  dialog: {
    colorScheme: {
      light: {
        maintextColor: "{zinc.900}",
      },
      dark: {
        maintextColor: "{zinc.100}",
      },
    },
  },
  card: {
    colorScheme: {
      light: {
        hoverBackground: "{zinc.100}",
        activeBackground: "{zinc.200}",
        color: "{surface.contrastColor}",
        border: "{zinc.300}",
        subtitleColor: "{zinc.600}",
      },
      dark: {
        background: "{surface.900}",
        hoverBackground: "{surface.800}",
        activeBackground: "{surface.700}",
        color: "{surface.contrastColor}",
        border: "{surface.700}",
        subtitleColor: "{zinc.400}",
      },
    },
  },
  select: {
    listPadding: "1rem",
  },
  button: {
    colorScheme: {
      light: {
        primary: {
          background: "{primary.color}",
          color: "{primary.contrastColor}",
          hoverBackground: "{primary.hoverColor}",
          hoverColor: "{primary.contrastColor}",
          activeBackground: "{primary.activeColor}",
          activeColor: "{primary.contrastColor}",
        },
        secondary: {
          background: "{secondary.color}",
          color: "{secondary.contrastColor}",
          hoverBackground: "{secondary.hoverColor}",
          hoverColor: "{secondary.contrastColor}",
          activeBackground: "{secondary.activeColor}",
          activeColor: "{secondary.contrastColor}",
        },
        textPrimaryHoverBackground: "{surface.100}",
      },
      dark: {
        primary: {
          background: "{primary.color}",
          color: "{primary.contrastColor}",
          hoverBackground: "{primary.hoverColor}",
          hoverColor: "{primary.contrastColor}",
          activeBackground: "{primary.activeColor}",
          activeColor: "{primary.contrastColor}",
        },
        secondary: {
          background: "{secondary.color}",
          color: "{secondary.contrastColor}",
          hoverBackground: "{secondary.hoverColor}",
          hoverColor: "{secondary.contrastColor}",
          activeBackground: "{secondary.activeColor}",
          activeColor: "{secondary.contrastColor}",
        },
      },
    },
  },
};
